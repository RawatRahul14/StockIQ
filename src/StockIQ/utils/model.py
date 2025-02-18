from dotenv import load_dotenv, find_dotenv
import os
from langchain.chat_models import ChatOpenAI

load_dotenv(find_dotenv())

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE")

def load_model():

    llm = ChatOpenAI(
        model_name = "deepseek-chat",
        temperature = 0,
        api_key = DEEPSEEK_API_KEY,
        base_url = DEEPSEEK_API_BASE,
        streaming = False
    )

    return llm