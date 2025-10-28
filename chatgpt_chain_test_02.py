from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv('.env')

prompt_template = ChatPromptTemplate.from_messages([
        ("system", "Du bist ein KI-Assistent der Englisch in eine andere Sprache übersetzt"),
        ("user", "Übersetze folgenden Text: '{input}' in {target_language}"),
     ])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = prompt_template | model | StrOutputParser() 

res = chain.invoke({"input": "I love programming.", "target_language": "German"})

print(res)