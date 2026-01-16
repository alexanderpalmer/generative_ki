import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from pprint import pprint
from langchain_text_splitters import RecursiveCharacterTextSplitter

import seaborn as sns
import matplotlib.pylab as plt

# Beschaffen des aktuellen Arbeitsverzeichnisses
file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(file_path)

# Wechsel ins Verzeichnis data, relativ vom Arbeitsverzeichnis
file_path = os.path.join(current_dir, "data", "HoundOfBaskerville.txt")

loader = TextLoader(file_path=file_path, encoding='utf-8')

docs = loader.load()

"""
Ein sehr wichtiger Parameter sind die Separatoren (separators).
Die Separatoren (oder auch Trennzeichen) sind eine Liste von Zeichen,
die verwendet werden, um die Trennungen zu erstellen. Sie sind vom 
größten zum kleinsten geordnet – wir beginnen also mit einem Separator
für Kapitel, dann für Unterkapitel und so weiter.
Wenn ein erster Split nicht ausreicht, um die Chunk-Größe auf das Limit
zu beschränken, wird nach einem weiteren Separator gesucht, 
um einen weiteren Split zu erzeugen. Dieser Prozess wird so lange
wiederholt, bis die Chunk-Größe innerhalb der vordefinierten Grenzen liegt
"""
splitter = RecursiveCharacterTextSplitter(
    chunk_size=256,
    chunk_overlap=50,
    separators=['\n\n' '\n', ' ', '.', ',']
)

docs_chunks = splitter.split_documents(docs)
print(len(docs_chunks))

chunk_length = [len(chunk.page_content) for chunk in docs_chunks]

sns.histplot(chunk_length, bins=50, binrange=(0,300))
plt.title('Verteilung der Chunk-Grössen (RecursiveChrakterTextSplitter)')
plt.xlabel('Anzahl der Zeichen')
plt.ylabel('Anzahl der Chunks')
plt.show()