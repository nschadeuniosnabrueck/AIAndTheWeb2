import logging
import os

import whoosh.index as index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

INDEX_FOLDER = 'stored_index'

# this code is executed every time something is imported why from this file, to ensure that the index exists
# create folder for index
if not os.path.exists(INDEX_FOLDER):
    os.mkdir(INDEX_FOLDER)

# create index if the folder is empty
if len(os.listdir(INDEX_FOLDER)) == 0:
    schema = Schema(title=TEXT(stored=True),
                    content=TEXT(stored=True),
                    url=ID(stored=True))  # we dont allow duplicates, so the url works as a ID
    ix = index.create_in(INDEX_FOLDER, schema)  # creates the index


def add_doc(data: dict) -> None:
    """
    Adds a document to the index
    :param data: document to add
    """
    # open index from the directory INDEX_FOLDER
    ind = index.open_dir(INDEX_FOLDER)
    update_url = ""
    # check if we already saved the url and update the index entry if we did
    with ind.searcher() as searcher:
        for doc in searcher.documents():
            # explicit if/elif for readability
            if data["url"] == doc["url"]:
                update_url = doc["url"]
            # different urls can redirect to the same page,
            # eg https://docs.python.org/3/../index.html and https://docs.python.org/3/index.html
            elif data["title"] == doc["title"] and data["url"].replace("../", "") == doc["url"].replace("../", ""):
                update_url = doc["url"]

    writer = ind.writer()
    try:
        if update_url != "":
            # using url as ID
            writer.delete_by_term('url', update_url)
        writer.add_document(title=data["title"], content=data["content"], url=update_url)
    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        # always close writer, even when an exception occurs
        writer.commit()


def search_word(words: str, limit: str) -> list:
    """
    Searches a string in the index and returns a list of results
    :param words: string to search for
    :param limit: number of results, 10 by default
    :return: list of results (title, url, content)
    """
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
