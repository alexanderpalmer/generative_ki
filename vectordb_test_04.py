import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from pprint import pprint
from langchain_text_splitters import CharacterTextSplitter

import seaborn as sns
import matplotlib.pylab as plt

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

splitter = CharacterTextSplitter(
    chunk_size=256,
    chunk_overlap=50,
    separator=" "
)

docs_chunks = splitter.split_documents(docs)
print(len(docs_chunks))

pprint(docs_chunks[100].page_content)
pprint(docs_chunks[101].page_content)

chunk_lengths = [len(chunk.page_content) for chunk in docs_chunks]

sns.histplot(chunk_lengths, bins=50, binrange=(100, 300))
# Titel hinzufügen
plt.title("Verteilung der Chunk-Grössen")
# Beschriftung der x-Achse
plt.xlabel("Anzahl der Zeichen")
# Beschriftung der y-Achse
plt.ylabel("Anzahl der Chunks")
plt.show()