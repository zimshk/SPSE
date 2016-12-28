#!/usr/local/bin/python3

import mechanicalsoup
import threading
import queue
from urllib.parse import urlparse

spider_site = "https://leifdreizler.com/"

br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})

page = br.get(spider_site)

top_level_links = {spider_site}

def crawl(page):
	parsed_domain = urlparse(spider_site)

	for link in [h.get('href') for h in page.soup.find_all('a')]:
		parsed_link = urlparse(link)

		if '#' in link:
			pass

		elif link.startswith('http'):
			if parsed_link.netloc == parsed_domain.netloc:
				top_level_links.add(link)
				print(f'Added link: {link}')

		elif link.startswith('/'):
			expanded_link = parsed_domain.scheme + "://" + parsed_domain.netloc + link
			top_level_links.add(expanded_link)
			print(f'{expanded_link}')


crawl(page)

for each in top_level_links:
	print(each)
	
print(top_level_links)