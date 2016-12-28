#!/usr/local/bin/python3
from suds.client import Client

"""Attack OWASP WebGoat Web Services
"""

# I had a lot of trouble getting newer versions of OWASP WebGoat to run with older "lessons" 
# which includes the Web Services Lesson (I think it was written in '05)
# I downloaded an OWASP WebGoat VM: https://sourceforge.net/projects/owaspbwa/files/

# Once you have WebGoat up and running, check out the WebServices lesson
# and complete the 'Create a SOAP Request' portion

# I used Burp Suite (free edition is fine) and this blog post
# https://blog.netspi.com/hacking-web-services-with-burp/
# to get a better understanding of what a webservice request looks like

# Like many of the libraries that Vivek recommends in Module 4, 
# ZSI is very old, and hasn't had any updates in a while
# I chose: https://github.com/cackharot/suds-py3 as my replacement

client = Client("http://10.0.0.171/WebGoat/services/SoapRequest?WSDL", username='guest', password='guest')


list_of_methods = [method for method in client.wsdl.services[0].ports[0].methods]

for method in list_of_methods:
    # dynamically create method calls
    method_to_call = getattr(client.service, method)
    
    for i in range(100, 105):
        result = method_to_call(i)
        
        if result:
            print("operation: {}, param: {}, result: {}".format(method, i, result))


# generic code for printing operation info: http://stackoverflow.com/a/1858144
# for method in client.wsdl.services[0].ports[0].methods.values():
#     print('%s(%s)' % (method.name, ', '.join('%s: %s' % (part.type, part.name) for part in method.soap.input.body.parts)))
