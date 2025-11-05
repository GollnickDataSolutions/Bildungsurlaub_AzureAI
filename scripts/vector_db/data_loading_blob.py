#%% packages
import os
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, BlobLoader
from azure.storage.blob import BlobClient, ContainerClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
#%% Azure Blob Storage configuration
CONNECTION_STRING = os.getenv("STORAGE_CONNECTION")
CONTAINER_NAME = "txtfiles"
container_client = ContainerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    container_name=CONTAINER_NAME
)

docs = []

for blob in container_client.list_blobs():
    print(blob.name)
    blob_client = BlobClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        container_name=CONTAINER_NAME,
        blob_name=blob.name
    )
    
    blob_content_bytes = blob_client.download_blob().readall()
    blob_content_str = blob_content_bytes.decode("utf-8")
    doc = Document(page_content=blob_content_str, metadata={"source": blob.name})
    docs.append(doc)


# %%
