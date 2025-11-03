#%% packages
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#%% You will need to set these environment variables or edit the following values.
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("OPENAI_API_VERSION", "2024-04-01-preview")
deployment = os.getenv("DEPLOYMENT_NAME", "dall-e-3")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)
#%% model inference
result = client.images.generate(
    model=deployment,
    prompt="Earth from international space station",
    n=1,
    style="natural",
    quality="standard",
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(image_url)
# %% download and save locall the image
import requests
response = requests.get(image_url)
with open("earth_from_iss.png", "wb") as f:
    f.write(response.content)

# %%
