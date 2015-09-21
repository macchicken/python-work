import socket
import random
import datetime

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port


def printServerInfo(message,clientAddress): # print information of server at each ping packet receive
	print 'Connected by ', clientAddress, 'at ', datetime.datetime.now()
	print 'Received message ', message

def udpServerFunc():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((HOST, PORT))
	while True:
		rand=random.randint(0, 10)
		try:
			message, clientAddress = s.recvfrom(2048)
			if not message: continue
		except socket.error:
			print 'receive error'
			continue
		printServerInfo(message, clientAddress)
		message=message.upper()
		if rand<4: continue # If rand is less is than 4, we consider the packet lost and do not respond
		s.sendto(message,clientAddress)
	s.close()

def tcpServerFunc():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)
	conn, addr = s.accept()
	while True:
		rand=random.randint(0, 10)
		try:
			message, (clientAddress,w) = conn.recvfrom(2048)
			if not message: conn.close();conn, addr = s.accept();continue
		except socket.error:
			print 'receive error'
			continue
		printServerInfo(message, addr)
		message=message.upper()
		if rand<4: continue # If rand is less is than 4, we consider the packet lost and do not respond
		conn.sendall(message)
	conn.close()


if __name__ == '__main__':
	udpServerFunc()
	# tcpServerFunc()
