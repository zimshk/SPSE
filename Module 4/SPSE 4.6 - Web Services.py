from selenium import webdriver
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Setup: Firefox 50, Selenium 3.0.2, Python 3.5.1
# You need to add the gecko webdriver somewhere in your $PATH
# https://github.com/mozilla/geckodriver/releases

driver = webdriver.Firefox()
driver.get("http://student.securitytube.net/login/index.php")
assert "Securitytube" in driver.title
driver.find_element_by_id("username").send_keys('''fill w/ your uname''')
driver.find_element_by_id("password").send_keys('''fill w/ your pw''')
driver.find_element_by_id("loginbtn").click()


