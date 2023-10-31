#!/usr/bin/env python3
from pydantic_settings import BaseSettings

from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI, AzureOpenAI
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()


def get_chat_openai():
    chat_openai = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
        # deployment_name='gpt35', 
        # model_name="gpt-35-turbo", 
        temperature=0
        )
    return chat_openai

def get_llm_openai():
    llm_openai = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        # deployment_name='gpt35',
        # model_name="gpt-35-turbo",
        temperature=0
        )
    return llm_openai

def get_embeddings():
    
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"),
                                chunk_size=10,   
                                # deployment='text-embedding-ada-002-bcai', 
                                # model="text-embedding-ada-002", 
        )
    return embeddings
# #################################
