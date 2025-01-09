# PySearch
## Description
This small project consists of a webcrawler (crawler.py) that crawls the [python3 documentation](https://docs.python.org/3/index.html). The documents are saved in an index (folder: stored_index) with their url, content and title.
The contents of the index are then made accessible via a flask webserver, where users can search for terms.  

## Project structure
- **template and static** folder belong to the flask frontend
- **stored_index** folder holds the crawled documents
- **index.py**: index functionality used by the crawler and webserver, the file itself does not have to be executed
- **crawler.py**: script used for crawling the python documentation, which has to be executed before information can be accessed via the webserver
- **webapp.py**: flask server with different endpoints
  - **/**: landing page
  - **/search**: page that displays the results

## Quickstart
Install requirements using `pip install -r requirements.txt`, then execute the crawler `python crawler.py`. The crawler will take a while to finish. Once the crawler is done, the webserver can be started using `python webapp.py` (in development, in production the server has to be properly deployed using .wsgi files). 