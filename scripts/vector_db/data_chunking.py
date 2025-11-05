#%% packages
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
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
