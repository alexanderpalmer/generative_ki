import ollama
from pprint import pprint

response = ollama.generate(model="gemma2:2b", prompt="Was ist ein LLM?")
pprint(response['response'])