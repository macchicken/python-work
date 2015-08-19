# Echo client program
import socket
import datetime
import time

HOST = 'localhost'    # The remote host
PORT = 12000          # The same port as used by the server
PINGTIMES=10		  # ping times used in the client


def udpClientFunc():
	mess=raw_input('what\'s your data?\n')
	for i in range(1,PINGTIMES+1):
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
		time.sleep(2)

def tcpClientFunc():
	mess=raw_input('what\'s your data?\n')
	for i in range(1,PINGTIMES+1):
		start = datetime.datetime.now()
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		clientSocket.settimeout(1) # time out 1 seconds for blocking method
		try:
			clientSocket.connect((HOST, PORT))
			clientSocket.sendall(mess)
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
		time.sleep(2)


if __name__ == '__main__':
	udpClientFunc()
	# tcpClientFunc()