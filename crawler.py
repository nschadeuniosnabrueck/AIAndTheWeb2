import requests
from bs4 import BeautifulSoup

prefix = 'https://vm009.rz.uos.de/crawl/'

start_url = prefix + 'index.html'

agenda = [start_url]
already_seen = []

while agenda:
    url = agenda.pop()
    already_seen.append(url)
    print("Get ", url)
    #request: library to perform web requests (to get html file)
    r = requests.get(url)
    print(r, r.encoding)
    if r.status_code == 200 and r.headers.get('Content-Type', '').lower() == 'text/html; charset=utf-8':
        #headers returns meta information (browser etc.)
        print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        #a: html element link
        all_links = soup.find_all('a')
        print(all_links)
        only_same_page_links = []
        for link in all_links:
            if not link['href'].startswith("http"):
                only_same_page_links.append(link)
        print (soup.text)
        for link in only_same_page_links:
            if prefix + link['href'] not in already_seen and prefix + link['href'] not in agenda:
                agenda.append(prefix + link['href'])


        print (f"Agenda= {agenda}")
        print (f"Already_seen={already_seen}")
