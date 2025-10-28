from langchain_classic import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from pprint import pprint

load_dotenv('.env')

prompt = hub.pull("hardkothari/prompt-maker")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = prompt | model | StrOutputParser()

lazy_prompt = "summer, vacation, beach"
task = "Shakespeare Gedicht in deutsch"

improved_prompt = chain.invoke({"lazy_prompt": lazy_prompt, "task": task})

res = model.invoke(improved_prompt)
print(res.content)