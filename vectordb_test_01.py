import os
from langchain_community.document_loaders import TextLoader

# Get the current working directory
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

file_path = os.path.join(current_dir, "data", "HoundOfBaskerville.txt")

text_loader = TextLoader(file_path=file_path, encoding="utf-8")
doc = text_loader.load()
print(doc[0].metadata)
print(doc[0].page_content)
