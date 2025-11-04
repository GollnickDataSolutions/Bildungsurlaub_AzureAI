#%% packages
import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from pydantic import BaseModel, Field
# %% structured output
class TranslationResponse(BaseModel):
    translated_text: str = Field(description="the translated text")
    detected_source_language: str = Field(description="the source language of the input text")

parser = PydanticOutputParser(pydantic_object=TranslationResponse)

# %% Prompt Template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant that translates a source language into a target languages. Strictly use only the provided format. {format_instructions}"),
    ("user", "der zu übersetzende Text: {source_text}; target language: {target_language}")
]).partial(format_instructions=parser.get_format_instructions())

#%% Model instance
endpoint = os.getenv("ENDPOINT_URL", "https://ai-bertgollnick9527ai080637128723.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o-mini")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
    deployment_name=deployment,
)

#%% chain setup
chain = prompt_template | model | parser

#%% chain invocation
res = chain.invoke({"source_text": "Hallo und herzlich Willkommen", "target_language": "französisch"})

# %% analyze output
# res.translated_text
res.detected_source_language

#%%
res
