import logging

import requests
from bs4 import BeautifulSoup

from index import add_doc

logging.basicConfig(filename="log.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO)


def extract(bs: BeautifulSoup, extract_url: str) -> dict:
    """
    Used to extract text from a BeautifulSoup object
    :param extract_url: url extracted from
    :param bs: BeautifulSoup object
    :return: dict containing title, content and url
    """
    title = str(bs.title.string) if bs.title else "No title"  # Falls kein Titel vorhanden
    content = bs.get_text()
    return {"title": title, "content": content, "url": extract_url}


def main():
    prefix = 'https://docs.python.org/3/'
    start = 'index.html'
    agenda = [prefix + start]
    # same as starting point
    already_seen = ["https://docs.python.org/3/"]
    sites_crawled = 0

    logging.info("Starting crawler at " + prefix + start)
    while agenda:
        url = agenda.pop()
        already_seen.append(url)
        # request: library to perform web requests (to get html file)
        try:
            r = requests.get(url)
            if r.status_code == 200 and r.headers.get('Content-Type', '').lower().startswith('text/html'):
                # headers returns meta information (browser etc.)
                soup = BeautifulSoup(r.content, 'html.parser')

                # Extract data and content
                data = extract(soup, url)
                add_doc(data)
                sites_crawled += 1
                if sites_crawled % 50 == 0:
                    logging.info(f"{sites_crawled} sites crawled, going on...")
                # a: html element link
                all_links = soup.find_all('a')
                only_same_page_links = []
                for link in all_links:
                    if '#' in link:
                        link = link.split('#')[0]
                    # skip links without href
                    if not link.has_attr('href'):
                        continue
                    if not link['href'].startswith("http") or link['href'].startswith(prefix):
                        only_same_page_links.append(link)
                for link in only_same_page_links:
                    new_url = prefix + link['href']
                    # we dont want to crawl captions of a page, because that would lead to duplicates
                    if '#' in new_url:
                        new_url = new_url.split('#')[0]
                    if new_url not in already_seen and new_url not in agenda:
                        agenda.append(new_url)
        # we catch any exception, so the crawler doesnt abort. we save the exception for troubleshooting later
        except Exception as e:
            logging.error(e)
    logging.info(f'{sites_crawled} sites crawled, finished.')


if __name__ == '__main__':
    main()
