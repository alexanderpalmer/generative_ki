import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv('.env')

MODEL_NAME = 'llama-3.3-70b-versatile'
model = ChatGroq(model_name=MODEL_NAME, 
                   temperature=0.5,
                   api_key=os.getenv('GROQ_API_KEY'))

res = model.invoke("Was ist Huggingface?")
res.dict()
print(res.dict())