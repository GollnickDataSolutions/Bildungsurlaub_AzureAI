#%% packages
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#%% azure
sample_text = "Hallo und herzlich willkommen in der Welt der Azure AI."
import requests

EMBEDDING_ENDPOINT_URI = os.getenv("EMBEDDING_ENDPOINT_URI")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY")

if not EMBEDDING_ENDPOINT_URI or not EMBEDDING_API_KEY:
    raise ValueError("Please set the EMBEDDING_ENDPOINT_URI and EMBEDDING_API_KEY environment variables.")

headers = {
    "Content-Type": "application/json",
    "api-key": EMBEDDING_API_KEY,
}

data = {
    "input": [sample_text]
}

response = requests.post(
    EMBEDDING_ENDPOINT_URI,
    headers=headers,
    json=data
)

if response.status_code == 200:
    embedding = response.json()["data"][0]["embedding"]
    print("Embedding:", embedding)
else:
    print("Failed to get embedding:", response.status_code, response.text)


# %%
len(embedding)
# %%
