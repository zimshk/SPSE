#!/usr/local/bin/python3

import socketserver
import threading

'''Code up the multi-threaded version of the SocketServer'''

# echo handler taken from 3.1 MT echo server + Vivek's 3.2 video
# threading taken from: https://pymotw.com/3/socketserver/#threading-and-forking

class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Got Connection from: {}".format(self.client_address))
        client = self.request

        while True:
            data = client.recv(2048)
            if data:   
                print("Client sent: {}".format(data))
                cur_thread = threading.currentThread()
                response = b'%s: %s' % (cur_thread.getName().encode(), data)
                client.sendall(response)
            else:
                print ("Closing connection...")
                client.close()
                return

class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


server = ThreadedEchoServer(("0.0.0.0", 9001), EchoHandler)
# similar to tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  from prev exercises
# allows quick reuse of the socket if you mess something up :-)
server.allow_reuse_address = True

threading.Thread(target=server.serve_forever).start()

