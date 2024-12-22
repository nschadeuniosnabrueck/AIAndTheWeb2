import requests
from bs4 import BeautifulSoup

from index import add_doc

prefix = 'https://vm009.rz.uos.de/crawl/'

start_url = prefix + 'index.html'

agenda = [start_url]
already_seen = []


def extract(bs: BeautifulSoup):
    """
    Used to extract text from a BeautifulSoup object
    :param bs: BeautifulSoup object
    :return: dict containing title and content
    """
    title = bs.title.string if bs.title else "No title"  # Falls kein Titel vorhanden
    content = bs.get_text()
    return {"title": title, "content": content}

while agenda:
    url = agenda.pop()
    already_seen.append(url)
    print("Get ", url)
    # request: library to perform web requests (to get html file)
    r = requests.get(url)
    print(r, r.encoding)
    if r.status_code == 200 and r.headers.get('Content-Type', '').lower().startswith('text/html'):
        # headers returns meta information (browser etc.)
        print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Extract data and content
        data = extract(url, soup)
        add_doc(data)

        # a: html element link
        all_links = soup.find_all('a')
        print(all_links)
        only_same_page_links = []
        for link in all_links:
            if not link['href'].startswith("http") or link['href'].startswith(prefix):
                only_same_page_links.append(link)
        print(soup.text)
        for link in only_same_page_links:
            if prefix + link['href'] not in already_seen and prefix + link['href'] not in agenda:
                agenda.append(prefix + link['href'])

        print(f"Agenda= {agenda}")
        print(f"Already_seen={already_seen}")
        print(f"data={data}")