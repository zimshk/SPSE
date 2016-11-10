#!/usr/bin/env python

import multiprocessing
import socket

'''Create a Multi-Threaded Echo Server'''

# multi-processing code from: https://pymotw.com/2/multiprocessing/basics.html
def simple_server(max_clients, port):
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # allow socket to be quickly reused in the event of an ungraceful exit
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
    tcpSocket.bind(("0.0.0.0", port))
    tcpSocket.listen(max_clients)

    return tcpSocket

def echo_handler(client, address):
    print("Waiting for a Client...")
    print("Received connection from: {}:{}".format(*address))
    print("Starting ECHO output...")

    while True:
        data = client.recv(2048)
        if data:
            print("Client sent: {}".format(data))
            client.send(data)
        else:
            print ("Closing connection...")
            client.close()
            return

tcpSocket = simple_server(3, 8000)
jobs = []

while True:
    client, address = tcpSocket.accept()
    p = multiprocessing.Process(target=echo_handler, args=(client, address))
    jobs.append(p)
    p.start()