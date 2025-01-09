import logging
import os

import whoosh.index as index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

INDEX_FOLDER = 'stored_index'

# create folder for index
if not os.path.exists(INDEX_FOLDER):
    os.mkdir(INDEX_FOLDER)

# create index
if len(os.listdir(INDEX_FOLDER)) == 0:
    schema = Schema(title=TEXT(stored=True),
                    content=TEXT(stored=True),
                    url=ID(stored=True))  # we dont allow duplicates, so the url works as a ID
    ix = index.create_in(INDEX_FOLDER, schema)  # creates the index


def add_doc(data):
    # open index from the directory INDEX_FOLDER
    ind = index.open_dir(INDEX_FOLDER)
    to_update = False
    with ind.searcher() as searcher:
        # Example 1: Iterating through all documents
        for doc in searcher.documents():
            if data["url"] == doc["url"]:
                to_update = True
    writer = ind.writer()
    try:
        if to_update:
            i = writer.delete_by_term('url', data["url"])
        writer.add_document(title=data["title"], content=data["content"], url=data["url"])
    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        # always close writer, even when an exception occurs
        writer.commit()


def search_word(words, limit):
    if limit.isdigit():
        limit = int(limit)
        if limit == 0:
            limit = 10
    else:
        limit = 10
    ind = index.open_dir(INDEX_FOLDER)
    qp = QueryParser("content", schema=ind.schema)
    q = qp.parse(words.encode("utf-8"))
    hit_list = []
    with ind.searcher() as searcher:
        res = searcher.search(q, limit=limit)
        # res contains Hits
        for hit in res:  #
            hit_list.append({"title": hit["title"], "url": hit["url"], "content": hit["content"]})
    return hit_list
