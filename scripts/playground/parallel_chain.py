#%% packages
import os
from pprint import pprint
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

#%% Prompt Template
messages_friendly = [
    ("system", "Du bist ein hilfreicher Assistent. Du antwortest immer kurz und freundlich"),
    ("user", "Thema: {topic}")
]

prompt_template_friendly = ChatPromptTemplate.from_messages(messages=messages_friendly)

messages_angry = [
    ("system", "Du bist ein hilfreicher Assistent. Du antwortest immer kurz und genervt"),
    ("user", "Thema: {topic}")
]

prompt_template_angry = ChatPromptTemplate.from_messages(messages=messages_angry)


#%% Initialize Azure OpenAI client with key-based authentication
model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)

#%% Chain
chain_friendly = prompt_template_friendly | model | StrOutputParser()
chain_angry = prompt_template_angry | model | StrOutputParser()

#%% invocation
map_chain = RunnableParallel(
    friendly=chain_friendly,
    angry=chain_angry,
)

res = map_chain.invoke({"topic": "Sinn des Lebens"})




#%% study response
pprint(res, width=40)
# %%
res.values()
