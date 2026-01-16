import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from pprint import pprint

# Beschaffen des aktuellen Arbeitsverzeichnisses
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Wechsel ins Verzeichnis data, relativ vom Arbeitsverzeichnis
text_files_path = os.path.join(current_dir, "data")

# Lade alle Dateien im definierten Verzeichnis
dir_loader = DirectoryLoader(path=text_files_path, glob="**/*.txt", 
                             loader_cls=TextLoader,
                             loader_kwargs={'encoding':'utf-8'}) 
docs = dir_loader.load()
for doc in docs:
    print(doc.metadata)