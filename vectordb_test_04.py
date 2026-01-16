"""
Dieses Beispiel lädt aus Wikipedia einige Dokumente
"""
from langchain_community.document_loaders import GutenbergLoader

# Details zum Buch
book_details = {
    'title': 'The Adventures of Sherlock Holmes',
    'author': 'Arthur Conan Doyle',
    'year': 1892,
    'language':'English',
    'genre':'Detective Fiction',
    'url':'https://www.gutenberg.org/cache/epub/1661/pg1661.txt' 
}

loader = GutenbergLoader(book_details.get('url'))
data = loader.load()

text = data[0].page_content

start_marker = '*** START OF THE PROJECT GUTENBERG EBOOK'
end_marker = '*** END OF THE PROJECT GUTENBERG EBOOK'

start_idx = text.find(start_marker)
end_idx   = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    raise ValueError("START/END Marker nicht gefunden – Format evtl. anders.")

# Ab dem Ende der START-Zeile schneiden
start_line_end = text.find("\n", start_idx)
book_text = text[start_line_end+1 : end_idx].strip()

print(book_text[:1500])