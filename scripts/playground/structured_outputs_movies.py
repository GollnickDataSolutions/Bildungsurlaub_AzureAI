#%% packages
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pydantic import BaseModel, Field
import json
from azure.storage.blob import BlobClient, ContainerClient
# %% structured output
class MyMovieOutput(BaseModel):
    title: str
    main_characters: list[str]
    director: str
    release_year: str

class MyMoviesOutput(BaseModel):
    movies: list[MyMovieOutput]

parser = PydanticOutputParser(pydantic_object=MyMoviesOutput)

# %% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein Filmexperte. Gib die Filme mit absteigender Reihenfolge nach kommerziellem Erfolg wider. Verwende strikt das vorgegebene Schema: {format_instructions}"),
    ("user", "Filmhandlung: {plot}, Anzahl der Filme: {movie_count}")
]).partial(format_instructions=parser.get_format_instructions())

#%% Model instance
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)

#%% chain setup
chain = prompt_template | model | parser

#%% chain invocation
res = chain.invoke({"plot": "ein sinkendes Schiff", "movie_count": 5})

# %% analyze output
for movie in res.movies:
    print(f"Titel: {movie.title}")
    print(f"Regisseur: {movie.director}")
    print(f"Erscheinungsjahr: {movie.release_year}")
    print("-"*20)

# %%
CONNECTION_STRING = os.getenv("STORAGE_CONNECTION")
CONTAINER_NAME = "movies"

#%%
for movie in res.movies:
    json_dump = json.dumps(movie.model_dump())
    BLOB_NAME = f"{movie.title}.json"
    blob_client = BlobClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        container_name=CONTAINER_NAME,
        blob_name=BLOB_NAME
    )
    blob_client.upload_blob(json_dump, overwrite=True, encoding="utf-8")    
    print(f"Blob {BLOB_NAME} erfolgreich erstellt")
# %% list files in container
container_client = ContainerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    container_name=CONTAINER_NAME
)
for blob in container_client.list_blobs():
    print(blob.name)