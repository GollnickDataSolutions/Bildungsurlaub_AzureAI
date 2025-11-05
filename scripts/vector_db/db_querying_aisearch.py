#%% packages
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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
endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")

#%% ai search invocation
def rag(user_query:str, k=3) -> str:
    # 1. Retrieval
    #-------------
    results = search_client.search(search_text=user_query, top=k)

    # show results
    res_list = []
    for res in results:
        print(res)
        res_list.append(res)

    # 2. Augmentation
    chunk_source_list = [f"Chunk: {res["chunk"]}, File: {res["title"]}"  for res in res_list]
    # convert list[str] in str
    context_info = ";".join(chunk_source_list)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
            Du bist Literaturexperte und kannst Fragen zu Romanen beantworten.
            Dir werden Kontextinformationen übergeben und du beantwortest du Nutzeranfrage ausschließlich auf Basis dieser Informationen.
            Wenn du die Frage nicht auf Basis des Kontextes beantworten kannst, sag 'Weiß ich doch auch'.
        """),
        ("user", "Nutzeranfrage: {user_prompt}, Kontextinformationen: {context_info}")
    ])

    # 3. Generation
    #--------------
    model = AzureChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version="2025-01-01-preview")

    # chain
    chain = prompt_template | model | StrOutputParser()

    # result
    res = chain.invoke({"user_prompt": user_query, "context_info": context_info})
    return res
# %%
rag(user_query="wer ist frankenstein?")