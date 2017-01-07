#!/usr/local/bin/python3

import mechanicalsoup
import threading
import queue
from urllib.parse import urlparse

def parse_links(page, domain):
    parsed_domain = urlparse(domain)
    links = {domain}

    for link in [h.get('href') for h in page.soup.find_all('a')]:
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
    top_level_links = parse_links(first_page, parent_url)

    if depth > 1:
        new_links = set()

        for i in range (depth):
            temp = new_links
            for link in top_level_links:
                br = mechanicalsoup.Browser(soup_config={'features':'lxml'})
                page = br.get(link)
                try:
                    page.soup # if page isn't html, this will fail
                    new_links |= parse_links(page, parent_url)
                except:
                    continue

            # if not finding any new links, but still have more depth, just break
            # because the site isn't deep enough
            if temp == new_links:
                break

            top_level_links |= new_links



    return top_level_links


parent_url = "https://leifdreizler.com/"
br = mechanicalsoup.Browser(soup_config={'features':'lxml'})
req = br.get(parent_url)

print(recursive_parse(req, parent_url, 5))
