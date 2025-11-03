#%% packages
import os
from pprint import pprint
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

#%% Prompt Template
messages = [
    ("system", "Du bist ein super Witzeerzähler und erzählst Witze zu einem gegebenen Thema."),
    ("user", "Thema: {topic}")
]

prompt_template = ChatPromptTemplate.from_messages(messages=messages)


#%% Initialize Azure OpenAI client with key-based authentication
model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)

#%% Chain
chain = prompt_template | model | StrOutputParser()

#%% invocation
res = chain.invoke({"topic": "Sommerurlaub"})

#%% study response
pprint(res, width=40)