from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import whoosh.index as index

# schema how the data will be stored in the index
schema = Schema(title=TEXT(stored=True), content=TEXT)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = index.create_in("indexdir", schema)

def add_doc(data):
    # Create an index in the directory indexdr (the directory must already exist!)
    ix = index.open_dir("indexdir")
    writer = ix.writer()
    writer.add_document(title=data["title"], content=data["content"])
    writer.commit()

def search_word(words):
    ix = index.open_dir("indexdir")
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(words)
    with ix.searcher() as searcher:
        res = searcher.search(q)
        print(res)

