#!/usr/local/bin/python3

import signal, os
import sys
import socket

'''
- Create a TCP server which listens to a port
- Implement signals to ensure it automatically shuts down after a pre-configured duration, which is given via command line
'''

# alarm code snippet: https://docs.python.org/2/library/signal.html#module-signal
# simple TCP server code from module 3-1

def handler(signum, frame):
	print('Signal handler called with signal'.format(signum))
	raise OSError("Server stopped!")

def simple_server():
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# allow socket to be quickly reused in the event of an ungraceful exit
	tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
	tcpSocket.bind(("0.0.0.0", 8000))
	tcpSocket.listen(2)

	print("Waiting for a Client...")

	(client, (ip,port)) = tcpSocket.accept()

	print("Received connection from: {}:{}".format(ip, port))

	print("Starting ECHO output...")

	data = 'dummy'

	while len(data):
	    data = client.recv(2048)
	    print("Client sent: {}".format(data))

	    client.send(data)

	print ("Closing connection...")
	client.close()

signal.signal(signal.SIGALRM, handler)
# no error handling, because yolo
signal.alarm(int(sys.argv[1]))

simple_server()

signal.alarm(0)          # Disable the alarm

