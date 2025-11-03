#%% packages
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

#%% keys and endpoints
service_endpoint = "https://search20251002.search.windows.net"
index_name = "shy-gyro-t0hw5mt8ny-index"
admin_key = os.getenv("AI_SEARCH_API_KEY")


#%% run search
credential = AzureKeyCredential(admin_key)
search_client = SearchClient(
    endpoint=service_endpoint,
    index_name=index_name,
    credential=credential
)

# --- Searching the Index ---
search_term = "generative KI"

results = search_client.search(search_text=search_term)
# %% show results
for result in results:
    print(result)