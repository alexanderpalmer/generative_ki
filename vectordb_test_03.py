"""
Dieses Beispiel lädt aus Wikipedia einige Dokumente
"""
from langchain_community.document_loaders import WikipediaLoader

# Zu ladende Artikel aus Wikipedia
articles = [
    {'title': 'Artificial Intelligence'},
    {'title': 'Artificial General Intelligence'},
    {'title': 'Superintelligence'},
]

# Laden aller Artikel
docs = []
for i in range(len(articles)):
    print(f"Lade Artikel von {articles[i].get('title')}")
    loader = WikipediaLoader(query=articles[i].get('title'),
                             lang='de',
                             load_all_available_meta=True,
                             doc_content_chars_max=100000,
                             load_max_docs=1)
    doc=loader.load()
    docs.extend(doc)
# Ausgabe des Titels des ersten Dokuments
print(docs[0].metadata.get('title'))

# Ausgabe der Quelle des ersten Dokuments
print(docs[0].metadata.get('source'))

# Ausgabe der Schlüsselworte des ersten Dokuments
print(docs[0].metadata.keys())

# Ausgabe des Inhalts des ersten Dokuments
print(docs[0].page_content)

# Ausgabe der ersten 500 Zeichen des Inhalts des ersten Dokuments
print(docs[0].page_content[:500])