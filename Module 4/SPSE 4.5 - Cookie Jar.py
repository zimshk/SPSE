import mechanicalsoup
import requests

"""Create an example to demonstrate the use of mechanize.CookieJar
"""

# I opted to use mechanicalsoup instead of mechanize

# I think the objective of this exercise is to show
# that you can take an active session from your browser
# and reuse that session in mechanicalsoup, or store
# a session and revisit it

br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})
login_page = br.get("http://student.securitytube.net/login/index.php")

form = login_page.soup.find('form')
form.select_one('#username')['value'] = # fill w/ your uname
form.select_one('#password')['value'] = # fill w/ your pw

landing_page = br.submit(form, login_page.url)

# Creates a new mechnicalsoup browser using the session from the original browser
# This allows you to view the student landing page without supplying creds
br2 = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, session = br.session)
landing_page2 = br2.get("http://student.securitytube.net/")

if (landing_page.text == landing_page2.text):
	print("Session successfully restored!")
