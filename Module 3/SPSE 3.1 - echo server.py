#!/usr/bin/python3

import socket

'''Create a simple Echo Server to handle 1 client'''

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

simple_server()
