#%% packages
import os
import base64
from pathlib import Path
from azure.ai.inference import EmbeddingsClient
from azure.ai.inference import ImageEmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import ImageEmbeddingInput
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# For Serverless API or Managed Compute endpoints
client = EmbeddingsClient(
    endpoint="https://ai-bertgollnick9527ai080637128723.services.ai.azure.com/models",
    credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_API_KEY"))
)
# %% embed text
model_name = "embed-v-4-0"
response = client.embed(
    input=["first phrase","second phrase","third phrase"],
    model=model_name
)
#%%
response.data[0].embedding

#%% embed image
#--------------
image_path = Path(__file__).parent / "kiki.jpg"
with open(image_path, "rb") as img_file:
    image_bytes = base64.b64encode(img_file.read()).decode('utf-8')
image_data_uri = f"data:image/jpeg;base64,{image_bytes}"

#%%
image_embeddings_client = ImageEmbeddingsClient(
        endpoint="https://ai-bertgollnick9527ai080637128723.services.ai.azure.com/models",
        credential=AzureKeyCredential(os.getenv("AZURE_OPENAI_API_KEY"))
    )

#%% create List[ImageEmbeddingInput] based on image_path
image_input = [ImageEmbeddingInput(image=image_data_uri)]
#%%
response = image_embeddings_client.embed(
    input=image_input,
    model=model_name
)
#%%
response.data[0].embedding