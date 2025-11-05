#%% packages
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%% embedding model instance
embeddings_model = AzureOpenAIEmbeddings(model="text-embedding-ada-002")

#%% vector db
db = Chroma(embedding_function=embeddings_model, persist_directory="vector_db_books")
# %%
retriever = db.as_retriever(kwargs={"search_type": "similarity", "k":5})

#%%
res = retriever.invoke("who is frankenstein?")

#%%
res[0].page_content