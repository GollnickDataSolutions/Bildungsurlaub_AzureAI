#%% packages
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#%%
credential = AzureKeyCredential(key=os.getenv("AI_SEARCH_API_KEY"))
search_client = SearchClient(
    endpoint=os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    index_name=os.getenv("AI_SEARCH_INDEX"),
    credential=credential
)

#%% ai search invocation
search_term = "Juliet"
results = search_client.search(search_text=search_term, top=3)


#%% show results
i = 0 
for res in results:
    print(res)
    i += 1

#%%
i

# %%
