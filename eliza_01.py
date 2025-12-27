from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console

console = Console()
load_dotenv(".env")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Session history
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

initial_prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein kreativer Geschichtenerzähler. "
    "           Basierend auf dem folgenden Kontext und der Wahl des Spielers setzt du die Geschichte fort und bietest dem Spieler drei neue Auswahlmöglichkeiten an. Halte die Geschichte extrem kurz und prägnant. Erstelle eine Eröffnungsszene für eine Abenteuergeschichte am Ort {place} und gib dem Spieler drei anfängliche Wahlmöglichkeiten.")
])

context_chain = initial_prompt | llm

config = {"configurable": {"session_id": "03"}}

llm_width_message_history = RunnableWithMessageHistory(context_chain, get_session_history=get_session_history)

context = llm_width_message_history.invoke({"place": "Ein dunkler Wald"}, config=config)

console.print(Markdown(context.content))

def process_player_choise(choise):
    response = llm_width_message_history.invoke([
        ("user", f"Führe die Geschichte auf Basis der Spielerwahl {choise} weiter",
         ("system", "Stelle dem Spieler drei neue Auswahlmöglichkeiten zur Verfügung"))
    ], config=config)
    return response

while True:
    player_choise = input("Gib deine Wahl ein (oder quit um das Spiel zu beenden)")
    if player_choise.lower() == "quit":
        break
    context = process_player_choise(player_choise)
    console.print(Markdown(context.content))
