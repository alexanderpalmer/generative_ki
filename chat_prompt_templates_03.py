# Beispiel, wie Chains in langchain funktionieren

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
load_dotenv('.env')

prompt_template = ChatPromptTemplate([
    ("system", "Du bist ein KI-Assistent welcher Englisch in eine andere Sprache übersetzt"),
    ("user", "Übersetze diesen Satz: '{input}' in '{target_language}'"),
])

# Modell bestimmen
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Verkettung festlegen (Chain)
chain = prompt_template | model | StrOutputParser()

# Verkettung ausführen (Invoking)
res = chain.invoke({"input": "I love programming", "target_language": "German"})

print(res)