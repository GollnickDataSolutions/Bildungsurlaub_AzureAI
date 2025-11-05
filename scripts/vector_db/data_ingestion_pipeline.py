#%% packages
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
file_path = os.path.abspath(__file__)
current_path = os.path.dirname(file_path)
data_path = os.path.join(current_path, "data")
data_path
# dir_path = ".\\data"

#%% 
loader = DirectoryLoader(path=data_path, loader_cls=TextLoader, glob="*.txt", loader_kwargs={'encoding': 'utf-8'})

docs = loader.load()
docs

#%% data chunking
# assumption: 1 token ~ 4 characters
splitter = CharacterTextSplitter(separator=" ", chunk_size=512*4, chunk_overlap=250)
docs_splitted = splitter.split_documents(docs)
len(docs_splitted)

#%%
splitter = RecursiveCharacterTextSplitter(separators=["\n\n\n\n", "\n\n", " ", ""], chunk_size=512*4, chunk_overlap=250)
docs_splitted = splitter.split_documents(docs)
len(docs_splitted)
#%% 
from pprint import pprint
pprint(docs[0].page_content)

#%% 
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma

#%% embedding model instance
embeddings_model = AzureOpenAIEmbeddings(model="text-embedding-ada-002")

#%% vector db
db = Chroma(embedding_function=embeddings_model, persist_directory="vector_db_books")
# %% add documents to db
import time
for i, doc in enumerate(docs_splitted):
    time.sleep(0.5)
    print(f"Füge aktuell Dokument {i}/{len(docs_splitted)} hinzu")
    db.add_documents([doc])


# %%
