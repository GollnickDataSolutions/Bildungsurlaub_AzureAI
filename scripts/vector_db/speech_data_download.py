#%% install the dataset: uv add datasets

#%%
from datasets import load_dataset

# Download the "MLCommons/peoples_speech" dataset into the "peoples_speech" subfolder
ds = load_dataset("parler-tts/mls_eng_10k")

# %%
