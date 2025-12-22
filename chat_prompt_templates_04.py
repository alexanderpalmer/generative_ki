# Beispiel, wie parallele Chains in langchain funktionieren

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pprint import pprint
load_dotenv('.env')

# Modell bestimmen
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Prompt definieren
polite_prompt = ChatPromptTemplate([
    ("system", "Du bist ein hilfreicher Assistent. Antworte in freundlicher und angenehmer Art"),
    ("human", "{topic}")
])

savage_prompt = ChatPromptTemplate([
    ("system", "Du bist ein hilfreicher Assistent. Antworte unfreundlicher und bösartiger Art"),
    ("human", "{topic}")
])

# Chains erstellen
polite_chain = polite_prompt | llm | StrOutputParser()
savage_chain = savage_prompt | llm | StrOutputParser()

# Vorbereiten für Parallele Ausführung
map_chain = RunnableParallel(
    polite=polite_chain,
    savage=savage_chain
)

topic = "Was ist der Sinn des Lebens?"
result = map_chain.invoke({"topic": topic})
pprint(result)