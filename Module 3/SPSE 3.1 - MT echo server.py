#!/usr/local/bin/python3

import threading
import socket

'''Create a Multi-Threaded Echo Server'''

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

# can connect using `ncat 127.0.0.1 8000` from multiple terminal tabs
tcpSocket = simple_server(3, 8000)

while True:
    client, address = tcpSocket.accept()
    threading.Thread(target=echo_handler, args=(client, address)).start()
