import azure.functions as func
import base64
import json
import logging
import os
from typing import List, Optional

import numpy as np

try:
    import onnxruntime as ort
except Exception as exc:  # pragma: no cover
    ort = None
    logging.error("onnxruntime failed to import: %s", exc)


app = func.FunctionApp()


# Load model once at cold start
_THIS_DIR = os.path.dirname(__file__)
_MODEL_PATH = os.path.join(_THIS_DIR, "model_lin_reg.onnx")

_ORT_SESSION: Optional["ort.InferenceSession"] = None
_INPUT_NAME: Optional[str] = None
_OUTPUT_NAMES: Optional[List[str]] = None


def _lazy_load() -> None:
    global _ORT_SESSION, _INPUT_NAME, _OUTPUT_NAMES
    if _ORT_SESSION is None:
        if ort is None:
            raise RuntimeError("onnxruntime is not available. Ensure it is installed.")
        if not os.path.exists(_MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {_MODEL_PATH}")
        _ORT_SESSION = ort.InferenceSession(_MODEL_PATH, providers=["CPUExecutionProvider"])  # CPU for local
        _INPUT_NAME = _ORT_SESSION.get_inputs()[0].name
        _OUTPUT_NAMES = [out.name for out in _ORT_SESSION.get_outputs()]


def _read_features_from_request(req: func.HttpRequest) -> np.ndarray:
    # Accept features via JSON {"features": [..37..]}, query "?features=csv", or raw body CSV
    ct = req.headers.get("content-type", "").lower()
    logging.info("Incoming content-type: %s", ct)
    features: Optional[List[float]] = None
    if ct.startswith("application/json"):
        try:
            data = req.get_json()
            if isinstance(data, dict) and isinstance(data.get("features"), list):
                features = [float(x) for x in data["features"]]
        except ValueError:
            pass
    if features is None:
        # Try query string
        qs = req.params.get("features")
        if qs:
            try:
                features = [float(x) for x in qs.split(",") if x.strip() != ""]
            except Exception:
                features = None
    if features is None:
        # Try raw body CSV
        body = req.get_body()
        if body:
            try:
                text = body.decode("utf-8", errors="ignore")
                features = [float(x) for x in text.split(",") if x.strip() != ""]
            except Exception:
                features = None
    if not features:
        raise ValueError("No features provided. Send JSON {\"features\": [..37..]} or CSV in body/query.")
    if len(features) != 37:
        raise ValueError(f"Expected 37 features, received {len(features)}.")
    arr = np.asarray(features, dtype=np.float32).reshape(1, 37)
    return arr


def _postprocess_numeric(output: np.ndarray) -> dict:
    arr = np.asarray(output)
    value = float(arr.reshape(-1)[0])
    return {"prediction": value}


@app.route(route="classify", auth_level=func.AuthLevel.ANONYMOUS)
def classify(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Classify endpoint invoked")
    try:
        _lazy_load()
        input_tensor = _read_features_from_request(req)
        outputs = _ORT_SESSION.run(_OUTPUT_NAMES, {_INPUT_NAME: input_tensor})  # type: ignore[arg-type]
        result = _postprocess_numeric(outputs[0])
        return func.HttpResponse(
            body=json.dumps({"success": True, "result": result}),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as exc:
        logging.exception("Classification failed: %s", exc)
        return func.HttpResponse(
            body=json.dumps({"success": False, "error": str(exc)}),
            status_code=400,
            mimetype="application/json",
        )


 