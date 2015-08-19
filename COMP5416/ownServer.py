import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 12000              # Arbitrary non-privileged port


def udpServerFunc():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((HOST, PORT))
	while True:
		message, clientAddress = s.recvfrom(2048)
		if not message: continue
		print 'Connected by ', clientAddress
		print 'message ', message
		message=message.upper()+" modified by server"
		s.sendto(message,clientAddress)
	s.close()

def tcpServerFunc():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)
	conn, addr = s.accept()
	while True:
		message, (w,clientAddress) = conn.recvfrom(2048)
		if not message: conn.close();conn, addr = s.accept();continue
		print 'Connected by ', clientAddress
		print 'message ', message
		message=message.upper()+" modified by server"
		conn.sendall(message)
	conn.close()


if __name__ == '__main__':
	udpServerFunc()
	# tcpServerFunc()
