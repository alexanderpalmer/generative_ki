from langchain_core.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Du bist ein KI-Assistent, der Englisch in eine andere Sprache übersetzt."),
    ("user", "Übersetze diesen Satz: '{input} into {target_language}"),
])

prompt_template.invoke({"input": "I love programming", "target_language": "German"})

print(prompt_template)