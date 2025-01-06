from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import whoosh.index as index

from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import RegexTokenizer, LowercaseFilter

# TODO also check if index exists, not just folder
if not os.path.exists("indexdir"):
    # Custom analyzer that doesn't remove stop words
    custom_analyzer = RegexTokenizer() | LowercaseFilter()
    schema = Schema(title=TEXT(stored=True, analyzer=custom_analyzer),
                    content=TEXT(stored=True, analyzer=custom_analyzer),
                    url=ID(stored=True)) # we dont allow duplicates, so the url works as a ID
    os.mkdir("indexdir")
    ix = index.create_in("indexdir", schema)  #creates the index


def add_doc(data):
    # Create an index in the directory indexdir (the directory must already exist!)
    ind = index.open_dir("indexdir")
    to_update = False
    with ind.searcher() as searcher:
        # Example 1: Iterating through all documents
        for doc in searcher.documents():
            if data["url"] == doc["url"]:
                print(data["url"], ' ', doc["url"])
                to_update = True
    writer = ind.writer()
    try:
        if to_update:
            i = writer.delete_by_term('url', data["url"])
            print(i)
        writer.add_document(title=data["title"], content=data["content"], url=data["url"])
    finally:
        # always close writer, even when an exception occurs
        writer.commit()


def search_word(words):
    ind = index.open_dir("indexdir")
    qp = QueryParser("content", schema=ind.schema)
    q = qp.parse(words.encode("utf-8"))
    hit_list = []
    with ind.searcher() as searcher:
        res = searcher.search(q)
        # res contains Hits
        for hit in res:
            print(hit)
            hit_list.append({"title": hit["title"], "url": hit["url"], "content":hit["content"]})
    return hit_list
