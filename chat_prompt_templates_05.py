from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utils.math import cosine_similarity
from dotenv import load_dotenv

load_dotenv('.env')

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings()

# Erstellen der Prompt Templates
template_math = "Löse das folgende mathematische Problem: {user_input}, verhalte dich wie ein Mathe-Agent"
template_music = "Empfehle einen Song für den Benutzer: {user_input}, verhalte dich wie ein Musik-Agent"
template_history = "Gib dem Benutzer eine Geschichtslektion zum Thema: {user_input}, verhalte dich wie ein Geschichtslehrer-Agent"

# Erstellen der einzelnen Chains
prompt_math = ChatPromptTemplate.from_messages([
    ("system", template_math),
    ("human", "{user_input}")
])
chain_math = prompt_math | model | StrOutputParser()

prompt_music = ChatPromptTemplate.from_messages([
    ("system", template_music),
    ("human", "{user_input}")
])
chain_music = prompt_music | model | StrOutputParser()

prompt_history = ChatPromptTemplate.from_messages([
    ("system", template_history),
    ("human", "{user_input}")
])
chain_history = prompt_history | model | StrOutputParser()

# Alle Chains in einer Liste ablegen
chains = [chain_math, chain_music, chain_history]

# Erstellen des Prompts für das Ebedding
chain_embeddings = embeddings.embed_documents(["math", "music", "history"])

# Prompt Router Funktion
def my_prompt_router(input: str):
    # embed the user input
    query_embedding = embeddings.embed_query(input)
    # berechnen der Ähnlichkeit
    similarities = cosine_similarity([query_embedding], chain_embeddings)
    # Beschaffung des Indes thes ähnlichsten Prompts
    most_similar_index = similarities.argmax()
    print("Index: ", most_similar_index)
    # Zurückgeben der entsprechenden Chain
    return chains[most_similar_index]

# Testen des Prompt Routers
# query = "Wer komponierte die Moonlight Sonate?"
query = "Was ist die Wurzel von 16?"
# query = "Was passierte während der französischen Revolution?"
chain = my_prompt_router(query)
answer = chain.invoke(query)
print(answer)
