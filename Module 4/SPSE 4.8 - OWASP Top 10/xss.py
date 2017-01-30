import mechanicalsoup

"create python scripts to test various entries of the OWASP Top 10"

'''I manually registered an account w/ xss in the "signature" form field, this script just checks for xss'''

br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})
login_page = br.get("http://192.168.1.228/mutillidae/index.php?page=login.php")

form = login_page.soup.find('form', id='idLoginForm')

form.select_one("[name=username]")['value'] = "toor"
form.select_one("[name=password]")['value'] = "toor"

landing_page = br.submit(form, login_page.url)

if "<script>alert(1)</script>" in landing_page.text:
	print("xss found!")
else:
	print("xss not found!")