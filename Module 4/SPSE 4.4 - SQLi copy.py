import mechanicalsoup

"""try SQLi on form fields and deduce which fields are vulnerable to SQLi
"""

# To test this you'll need a vulnerable webapp
# https://www.owasp.org/index.php/OWASP_Vulnerable_Web_Applications_Directory_Project#tab=On-Line_apps

# I initially chose OWASP Webgoat, but mechsoup was having issues w/ the JS
# I recommend using: http://demo.testfire.net/ creds=jsmith/Demo1234

attack_string = "' OR 1=1;-"
safe_string = "asdf"
br = mechanicalsoup.Browser(soup_config={'features': 'lxml'})

# login_page = br.get("http://demo.testfire.net/bank/login.aspx")
login_page = br.get("http://demo.testfire.net/feedback.aspx")

forms = login_page.soup.find_all('form')
print(len(forms)); exit(1)

for form in forms:
	# removes the type=submit input tags
	inputs = [x for x in form.findChildren('input') if x.has_attr('id')]
	
	# uses a nested loop to test each form field individually
	# while still submitting safe values for the other fields in the same form

	for i,input in enumerate(inputs):
		for j in range(len(inputs)):
			#print("i: {} -- form: {}".format(i, form.findChildren('input')[i]))
			print("i: {} -- j: {} -- form: {}".format(i, j, form.select('input')[i]))
			#print(form.select('input')[i])
		#	if i == j:
		#		form.select('input')[i]['value'] = attack_string


	#print(inputs)

	#	print(form['id'] + "  " + str(input))
	   



	    # if input.has_attr('id'):
	    #     login_form.select_one(input['id'])['value'] = attack_string

# login_form.select_one("#passw")['value'] = 'Demo1234'
# page2 = br.submit(login_form, login_page.url)
