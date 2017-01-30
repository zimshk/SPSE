import mechanicalsoup

"create python scripts to test various entries of the OWASP Top 10"

br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})
login_page = br.get("http://192.168.1.228/mutillidae/index.php?page=login.php")

login_form = login_page.soup.find('form', id='idLoginForm')


if login_form.find("input", {"name":"csrf-token"}) == None:
	print("No CSRF protection in place!")

elif login_form.find("input", {"name":"csrf-token"})["value"] == "":
	print("No CSRF protection in place!")
