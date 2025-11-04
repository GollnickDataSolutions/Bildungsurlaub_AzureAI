#%% packages
import os
from pprint import pprint
from langchain_openai import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utils.math import cosine_similarity
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

#%% Initialize Azure OpenAI client with key-based authentication
model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)
#%% 
messages_math = [
    ("system", """
     Du bist ein hilfreicher Nachhilfelehrer. 
     Du antwortest immer freundlich und bist spezialisiert auf Mathematik.
     Gib an, dass du ein 'Mathe-Tutor' bist.
     """),
    ("user", "Thema: {topic}")
]

prompt_template_math = ChatPromptTemplate.from_messages(messages=messages_math)

chain_math = prompt_template_math | model | StrOutputParser()

messages_music = [
    ("system", """
     Du bist ein hilfreicher Nachhilfelehrer. 
     Du antwortest immer freundlich und bist spezialisiert auf Musik.
     Gib an, dass du ein 'Musik-Tutor' bist.
     """),
    ("user", "Thema: {topic}")
]

prompt_template_music = ChatPromptTemplate.from_messages(messages=messages_music)

chain_music = prompt_template_music | model | StrOutputParser()

messages_history = [
    ("system", """
     Du bist ein hilfreicher Nachhilfelehrer. 
     Du antwortest immer freundlich und bist spezialisiert auf Geschichte.
     Gib an, dass du ein 'Geschichtstutor' bist.
     """),
    ("user", "Thema: {topic}")
]

prompt_template_history = ChatPromptTemplate.from_messages(messages=messages_history)

chain_history = prompt_template_history | model | StrOutputParser()

#%% embedding model
embedding_model = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_key=os.getenv("EMBEDDING_API_KEY")
)

chain_embeddings = embedding_model.embed_documents(texts=['Mathematik', 'Musik', 'Geschichte'])

#%%
chain = [chain_math, chain_music, chain_history]

#%%
def my_router(user_query: str = "Erzähl mir über den 30 jährigen Krieg"):
    user_query_embedding = embedding_model.embed_query(user_query)

    # Analysiere die Ähnlichkeiten
    # user_query_embedding -> (1536,) ! benötigt ist (1, 1536)
    # chain_embeddings -> (3, 1536)

    similarities = cosine_similarity([user_query_embedding], chain_embeddings)
    most_similar_index = similarities.argmax()
    return chain[most_similar_index]

#%% Test
# query = "wer sind die rolling stones"
query = "wann war die französische Revolution"
selected_chain = my_router(user_query=query)
selected_chain.invoke({"topic": query})














# %%
