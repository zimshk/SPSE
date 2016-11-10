#!/usr/local/bin/python3

import select
import socket
import sys
import queue

# select() code from: http://ilab.cs.byu.edu/python/select/echoserver.html
# TCP server code from: 3-1 echo server

def simple_server(max_clients, port):
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # allow socket to be quickly reused in the event of an ungraceful exit      
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    tcpSocket.setblocking(0)
    tcpSocket.bind(("0.0.0.0", port))
    tcpSocket.listen(max_clients)

    return tcpSocket

server = simple_server(3, 8000)

input = [server]

while True: 
    inputready,outputready,exceptready = select.select(input,[],[]) 

    for s in inputready: 
        if s == server: 
            # handle the server socket 
            client, address = server.accept() 
            input.append(client) 
            
        else: 
            # handle all other sockets 
            data = s.recv(2048) 
            if data: 
                s.send(data) 
            else: 
                s.close() 
                input.remove(s) 

server.close()
