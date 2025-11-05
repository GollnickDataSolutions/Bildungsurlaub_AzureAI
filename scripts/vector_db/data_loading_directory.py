#%% packages
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader

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
