import signal, os
import sys
import socket

'''Create a TCP server which listens to a port; Implement signals to ensure it automatically shuts down after a pre-configured duration, which is given via command line'''

# alarm code snippet: https://docs.python.org/2/library/signal.html#module-signal
# simple TCP server code: http://www.binarytides.com/python-socket-server-code-example/

def handler(signum, frame):
	print('Signal handler called with signal'.format(signum))
	raise OSError("Server stopped!")

def simple_server(): 
	HOST = ''   # Symbolic name, meaning all available interfaces
	PORT = 8888 # Arbitrary non-privileged port

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Socket created')

	#Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	print('Socket bind complete')

	#Start listening on socket
	s.listen(10)
	print('Socket now listening')

	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])

	s.close()

signal.signal(signal.SIGALRM, handler)
# no error handling, because yolo
signal.alarm(int(sys.argv[1]))

simple_server()

signal.alarm(0)          # Disable the alarm

