import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv('.env')

MODEL_NAME = 'gpt-4o-mini'
model = ChatOpenAI(model_name=MODEL_NAME, 
                   temperature=0.5,
                   api_key=os.getenv('OPENAI_API_KEY'))

res = model.invoke("Was ist LangChain?")
res.dict()
print(res.dict())