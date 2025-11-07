import azure.functions as func
import json
import logging
import onnxruntime as ort
from PIL import Image
import numpy as np
import io
import requests

app = func.FunctionApp()

# Load ONNX model at module level
session = ort.InferenceSession(
    "bin_class_model.onnx",
    providers=["CPUExecutionProvider"],
)

@app.route(route="predict", auth_level=func.AuthLevel.ANONYMOUS)
def predict(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python predict function processed a request.')

    # Get image_url from query params or request body
    image_url = req.params.get('image_url')
    if not image_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            image_url = req_body.get('image_url') if req_body else None

    if not image_url:
        return func.HttpResponse(
            json.dumps({"error": "image_url parameter is required"}),
            status_code=400,
            mimetype="application/json"
        )

    # Download image
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }
        resp = requests.get(str(image_url), timeout=15, headers=headers)
        resp.raise_for_status()
        image_bytes = resp.content
    except Exception as e:
        logging.error(f"Failed to download image: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to download image: {e}"}),
            status_code=400,
            mimetype="application/json"
        )

    # Preprocess image
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L")
        img = img.resize((32, 32))
        arr = np.array(img).astype(np.float32) / 255.0
        arr = (arr - 0.5) / 0.5
        arr = np.expand_dims(arr, axis=0)
        arr = np.expand_dims(arr, axis=0)
    except Exception as e:
        logging.error(f"Failed to preprocess image: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to preprocess image: {e}"}),
            status_code=400,
            mimetype="application/json"
        )

    # Run inference
    try:
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        logits = session.run([output_name], {input_name: arr})[0]
        logit = float(logits[0][0])
        prob = 1.0 / (1.0 + np.exp(-logit))
        label = "chihuahua" if prob > 0.5 else "muffin"

        result = {
            "label": label,
            "prob_chihuahua": float(prob),
            "prob_muffin": float(1.0 - prob)
        }

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Failed to run inference: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"Failed to run inference: {e}"}),
            status_code=500,
            mimetype="application/json"
        )