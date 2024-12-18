from whoosh.index import create_in
from whoosh.fields import *

# schema how the data will be stored in the index
schema = Schema(title=TEXT(stored=True), content=TEXT)

# Create an index in the directory indexdr (the directory must already exist!)
ix = create_in("indexdir", schema)
writer = ix.writer()

def extract(url, soup):
    title = soup.title.string if soup.title else "No title"  # Falls kein Titel vorhanden
    content = soup.get_text()
    return {"title": title, "content": content}


def add_doc(data):
    writer.add_document(title=data["title"], content=data["content"])

