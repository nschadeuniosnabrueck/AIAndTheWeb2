import requests
from bs4 import BeautifulSoup
from weblogger import log

from index import add_doc


def extract(bs: BeautifulSoup, extract_url: str):
    """
    Used to extract text from a BeautifulSoup object
    :param extract_url: url extracted from
    :param bs: BeautifulSoup object
    :return: dict containing title and content
    """
    title = str(bs.title.string) if bs.title else "No title"  # Falls kein Titel vorhanden
    content = bs.get_text()
    return {"title": title, "content": content, "url": extract_url}


def main():
    prefix = 'https://docs.python.org/3/'
    agenda = [prefix]
    already_seen = []
    sites_crawled = 0

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
                    if '#' in new_url:
                        new_url = new_url.split('#')[0]
                    if new_url not in already_seen and new_url not in agenda:
                        print(new_url)
                        agenda.append(new_url)
        # we catch any exception, so the crawler doesnt abort. we save the url for troubleshooting later
        except:
            log(f'Exception while fetching {url}', True)
    log(f'{sites_crawled} sites crawled')


if __name__ == '__main__':
    main()
