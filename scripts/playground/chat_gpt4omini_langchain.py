#%% packages
import os
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

# Initialize Azure OpenAI client with key-based authentication
model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)

#%% Prepare the chat prompt
model.invoke("Was ist Bildungsurlaub?")