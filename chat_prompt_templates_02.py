# Im Buch steht from langchain import hub, aber neu ist hub in langchain_classic organisiert
from langchain_classic import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv('.env')
from pprint import pprint

prompt = hub.pull("hardkothari/prompt-maker")

# Modell bestimmen
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Chain definieren
chain = prompt | model | StrOutputParser()

# Chain ausführen (invoke)
lazy_prompt = "Sommer, Ferien, Strand"
task ="Shakespeare Gedicht"
improved_prompt = chain.invoke({"lazy_prompt": lazy_prompt, "task": task})
# print (improved_prompt)

# Run Model mit dem verbesserten Prompt
res = model.invoke(improved_prompt)
print(res.content)
