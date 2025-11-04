#%% packages
import os
import pickle
import json
from azure.storage.blob import BlobClient, ContainerClient
#%%
data_object = {"name": "Test", "value": 123} 
json_string = json.dumps(data_object)

# %%
CONNECTION_STRING = "..."
CONTAINER_NAME = "docs"
BLOB_NAME = "your_object_name.pkl" 

# 1. Create a BlobClient
blob_client = BlobClient.from_connection_string(
    conn_str=CONNECTION_STRING, 
    container_name=CONTAINER_NAME, 
    blob_name=BLOB_NAME
)

# 2. Upload the serialized data (byte string)
# The data is treated as binary data, which is suitable for pickle output.
blob_client.upload_blob(json_string, overwrite=True, encoding='utf-8')

print(f"Object uploaded to Azure Blob: {BLOB_NAME}")
# %% list all files in blob
blob_client.list_page_ranges()

# %% list all files in blob
# To list blobs, you need to use a ContainerClient, not BlobClient
container_client = ContainerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    container_name=CONTAINER_NAME
)

print("Blobs in the container:")
for blob in container_client.list_blobs():
    print(blob.name)

# %%
