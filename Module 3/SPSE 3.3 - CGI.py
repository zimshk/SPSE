#!/usr/local/bin/python3

import socketserver
import http.server

'''Write a module to run CGI instead of SimpleHTTPServer'''

# python3 -m http.server --cgi

'''
there are some naming differences between python 2 and 3
so I wanted to use this exercise as a way to demonstrate 
how to use http.server in python3. You also need to write things 
bytes instead of strings when replying to the client.
'''

class HttpRequestHandler (http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/admin':
			self.wfile.write('This page is only for Admins!\n\n'.encode('utf-8'))
			self.wfile.write((str(self.headers).encode('utf-8')))
		else:
			http.server.SimpleHTTPRequestHandler.do_GET(self)


httpServer = socketserver.TCPServer(("0.0.0.0", 10000), HttpRequestHandler)
httpServer.allow_reuse_address = True
httpServer.serve_forever()