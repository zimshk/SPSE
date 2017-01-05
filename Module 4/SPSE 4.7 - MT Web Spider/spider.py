#!/usr/local/bin/python3

import bs4
import requests
import threading
import queue
from urllib.parse import urlparse

def parse_links(page, domain):
    parsed_domain = urlparse(domain)
    links = {domain}

    for link in [h.get('href') for h in page.find_all('a', href=True)]:
        parsed_link = urlparse(link)

        if '#' in link:
            pass

        elif link.startswith('http'):
            if parsed_link.netloc == parsed_domain.netloc: # stops spider from going "off-site"
                links.add(link)

        elif link.startswith('/'):
            expanded_link = parsed_domain.scheme + "://" + parsed_domain.netloc + link
            links.add(expanded_link)

    return links

def recursive_parse(first_page, domain, depth):

    if depth > 1:
        top_level_links = parse_links(start_page, parent_url)
        new_links = set()

        for link in top_level_links:
            req = requests.get(link).text
            page = bs4.BeautifulSoup(req, "lxml", parse_only=bs4.SoupStrainer('a', href=True))
            new_links |= parse_links(page, parent_url)

        # TODO: add recursive call and depth checking

    else:
        return top_level_links = parse_links(start_page, parent_url)


print(new_links)

parent_url = "https://leifdreizler.com/"
req = requests.get(parent_url).text
start_page = bs4.BeautifulSoup(req, "lxml", parse_only=bs4.SoupStrainer('a', href=True))

recursive_parse(start_page, parent_url, 1)