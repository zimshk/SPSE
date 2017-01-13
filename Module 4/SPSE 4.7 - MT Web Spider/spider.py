#!/usr/local/bin/python3

import mechanicalsoup
from joblib import Parallel, delayed
from urllib.parse import urlparse
import psycopg2

'''Create a Multi-Threaded Web Spider which – takes a website and depth of spidering as input – download the HTML files only
– Inserts the HTML into a MySQL Database
– It also parses the Forms on each page'''

# I did this exercise w/ postgresql instead because I wanted to learn a bit of postgresql instead
# I found this tutorial helpful: https://www.fullstackpython.com/blog/postgresql-python-3-psycopg2-ubuntu-1604.html

# setup postgresql DB
# replace the dbname user and password w/ your
try:
    connect_str = "dbname='#' user='#' host='localhost' password='#'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE html (url varchar, source text);")
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)


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

def parallelize_links(link):
    br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})
    page = br.get(link)
    
    try:
        page.soup  # if page isn't html, this will fail
        return [link, page.content, parse_links(page, parent_url)]
    except:
        return ["", "", set()]

def recursive_parse(first_page, domain, depth):
    top_level_links = parse_links(first_page, parent_url)

    if depth > 1:
        new_links = set()

        for i in range (depth):
            temp = new_links

            # results is the [url, html source, and the links from that page]
            results = Parallel(n_jobs=2)(delayed(parallelize_links)(link) for link in top_level_links)
            
            for result in results:
                # if results[0] is nothing, then all the values are empty
                if(result[0]):
                    cursor.execute("INSERT INTO html (url, source) VALUES (%s, %s)", (result[0], result[1]))
                    new_links |= result[2]


            if temp == new_links:
                break

            top_level_links |= new_links



    return top_level_links




parent_url = "https://leifdreizler.com/"
br = mechanicalsoup.Browser(soup_config={'features':'lxml'})
req = br.get(parent_url)

recursive_parse(req, parent_url, 5)

cursor.execute("SELECT * FROM html;")
rows = cursor.fetchall()
print(rows)