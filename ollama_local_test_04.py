from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 1) Chat & Prompt
chat = ChatOllama(model="gemma2:2b", temperature=0.2)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein hilfreicher, freundlicher Assistent auf Deutsch."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])
chain = prompt | chat

# 2) Session Memory-Store (hier: in-memory dict)
store = {}  # {session_id: InMemoryChatMessageHistory}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 3) Chain mit MessageHistory „umwickeln“
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# 4) Nutzung (pro Sitzung)
cfg = {"configurable": {"session_id": "alex-session-1"}}

res1 = chain_with_history.invoke({"input": "Was ist ein LLM?"}, cfg)
print("Antwort 1:", res1.content)

res2 = chain_with_history.invoke({"input": "Gib mir bitte eine 2-Satz-Zusammenfassung."}, cfg)
print("\nAntwort 2:", res2.content)

# Metadaten
print("\nResponse-Metadaten:", res2.response_metadata)
print("Usage-Metadaten:", res2.usage_metadata)

# Vollständiges Objekt (statt veraltetem .dict()):
print("\nDump (kompakt):", res2.model_dump(exclude_none=True))
