# Echo client program
import socket
import datetime

HOST = 'localhost'    # The remote host
PORT = 12000          # The same port as used by the server
PINGTIMES=10		  # ping times used in the client


def udpClientFunc():
	for i in range(1,PINGTIMES+1):
		mess=raw_input('what\'s your data?\n')
		start = datetime.datetime.now()
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientSocket.settimeout(1) # time out 1 seconds for blocking method
		clientSocket.sendto(mess,(HOST,PORT))
		try:
			modifiedMessage,(serverAddress,w) = clientSocket.recvfrom(2048)
			print 'server address ', serverAddress
			print 'Received', repr(modifiedMessage)
			end = datetime.datetime.now()
			interval=end-start
			print 'round trip time ',int(interval.total_seconds() * 1000)
		except socket.timeout:
			print 'Request time out'
		except socket.error:
			print 'remote server error'
		clientSocket.close()

def tcpClientFunc():
	for i in range(1,PINGTIMES+1):
		mess=raw_input('what\'s your data?\n')
		start = datetime.datetime.now()
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientSocket.settimeout(1) # time out 1 seconds for blocking method
		clientSocket.connect((HOST, PORT))
		clientSocket.sendall(mess)
		try:
			modifiedMessage,(serverAddress,w) = clientSocket.recvfrom(2048)
			print 'server address ', serverAddress
			print 'Received', repr(modifiedMessage)
			end = datetime.datetime.now()
			interval=end-start
			print 'round trip time ',int(interval.total_seconds() * 1000)
		except socket.timeout:
			print 'Request time out'
		except socket.error:
			print 'remote server error'
		clientSocket.close()


if __name__ == '__main__':
	# udpClientFunc()
	tcpClientFunc()