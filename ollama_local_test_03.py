from langchain_ollama import ChatOllama

llm = ChatOllama(model="gemma2:2b")
# llm = ChatOllama(model="gemma3:4b")
response = llm.invoke("Was ist ein LLM?")
print("Antwort: ",response.content)
print("Mettadaten: ", response.model_dump())