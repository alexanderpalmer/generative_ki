from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utils.math import cosine_similarity
from dotenv import load_dotenv

load_dotenv('.env')

# Model and Ebedding Setup
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings()

# Prompt Templates
template_math = "Löse das folgende mathematische Problem: {user_input} verhalte dich wie ein Mathematik-Agent"

template_music = "Empfehle einen Song für den Benutzer: {user_input}, verhalte dich wie ein Musik-Agent"

template_history = "Geben Sie dem Benutzer eine Geschichtsstunde_ {user_input}, verhalte dich wie ein Geschichts-Agent"

prompt_math = ChatPromptTemplate.from_messages([
    ("system", template_math),
    ("human", "{user_input}")
])

