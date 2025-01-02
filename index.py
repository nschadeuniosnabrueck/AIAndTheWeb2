from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import whoosh.index as index

# schema how the data will be stored in the index, will only be played one time now
# TODO also check if index exists, not just folder
if not os.path.exists("indexdir"):
    schema = Schema(title=TEXT(stored=True), content=TEXT, url=TEXT(stored=True))
    os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema) #erstellt den index

def add_doc(data):
    # Create an index in the directory indexdir (the directory must already exist!)
    ind = index.open_dir("indexdir")
    writer = ind.writer()
    writer.add_document(title=data["title"], content=data["content"], url=data["url"])
    writer.commit()

def search_word(words):
    ind = index.open_dir("indexdir")
    qp = QueryParser("content", schema=ind.schema)
    q = qp.parse(words.encode("utf-8"))
    urls = []
    with ind.searcher() as searcher:
        res = searcher.search(q)
        # res contains Hits
        for hit in res:
            urls.append(hit["url"])
    return urls

