from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import whoosh.index as index

from whoosh.fields import Schema, TEXT
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter

# TODO also check if index exists, not just folder
if not os.path.exists("indexdir"):
    # Custom analyzer that doesn't remove stop words
    custom_analyzer = StopFilter(stoplist=[])
    schema = Schema(title=TEXT(stored=True, analyzer = custom_analyzer), content=TEXT(stored=True, analyzer=custom_analyzer), url=TEXT(stored=True))
    os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema) #creates the index


def add_doc(data):
    # Create an index in the directory indexdir (the directory must already exist!)
    ind = index.open_dir("indexdir")
    with ind.searcher() as searcher:
        # Example 1: Iterating through all documents
        for doc in searcher.documents():
            if data["url"] == doc["url"]:
                return
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

