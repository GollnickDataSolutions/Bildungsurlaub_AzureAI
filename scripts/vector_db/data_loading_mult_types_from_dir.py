#%% packages
import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyMuPDFLoader

#%%
file_path = os.path.abspath(__file__)
current_path = os.path.dirname(file_path)
data_path = os.path.join(current_path, "data")
data_path
# dir_path = ".\\data"

#%% function for different file types
def select_loader(file_path):
    _, ext =os.path.splitext(file_path)
    if ext == ".txt":
        return TextLoader(file_path=file_path, encoding="utf-8")
    if ext == ".pdf":
        return PyMuPDFLoader(file_path=file_path, mode="single")
    raise ValueError(f"Unsupported file type: {ext} for {file_path}")


#%% directory loader
loader = DirectoryLoader(path=data_path, loader_cls=select_loader, show_progress=True)

docs = loader.load()
docs

# %%
