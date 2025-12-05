from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pprint import pprint

load_dotenv('.env')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

#example: style variations (friendly, polite) vs. (savage, angry)
polite_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bust ein hilfsbereiter Assistent. Antworte freundlich und höflich."),
    ("human", "{topic}")
])

savage_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfsbereiter Assistent. Antworte brutal und unhöflich"),
    ("human", "{topic}")
])

# chaining 
polite_chain = polite_prompt | llm | StrOutputParser()
savage_chain = savage_prompt | llm | StrOutputParser()

# parallelism
map_chain = RunnableParallel(
    polite=polite_chain,
    savage=savage_chain
)

# invoking
topic = "Was ist der Sinn des Lebens?"
result = map_chain.invoke({"topic":topic})
pprint(result)