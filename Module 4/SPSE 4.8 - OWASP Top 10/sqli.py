import mechanicalsoup

"create python scripts to test various entries of the OWASP Top 10"

br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})
login_page = br.get("http://192.168.1.228/mutillidae/index.php?page=login.php")

form = login_page.soup.find('form', id='idLoginForm')

form.select_one("[name=username]")['value'] = "test"
form.select_one("[name=password]")['value'] = "'"

landing_page = br.submit(form, login_page.url)

if "SQL syntax" in landing_page.text:
	print("SQLi found!")
else:
	print("SQLi not found!")