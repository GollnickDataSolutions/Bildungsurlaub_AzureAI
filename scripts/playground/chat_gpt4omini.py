#%% packages
import os
import base64
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant and answer like Shakespeare."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Was ist Bildungsurlaub?"
            }]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

# Generate the completion
completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=6553,
    temperature=0.42,
    top_p=0.92,
    frequency_penalty=2,
    presence_penalty=0,
    stop=None,
    stream=False
)
#%%
print(completion.to_json())
# %%
