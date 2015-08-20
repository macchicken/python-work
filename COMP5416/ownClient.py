# Echo client program
import socket
import datetime
import time
import decimal

HOST = 'localhost'    # The remote host 192.241.218.95
PORT = 12000          # The same port as used by the server
PINGTIMES=10		  # ping times used in the client
rtts=[]				  # list of rtt of each ping


def printClientInfo(modifiedMessage,serverAddress,startTime): # print information of client at each ping
	print 'server address=', serverAddress
	print 'Received=', repr(modifiedMessage)
	end = datetime.datetime.now()
	interval=end-startTime
	rtt=int(interval.total_seconds()*1000)
	print 'round trip time=',rtt
	rtts.append(rtt)

def stats(): # report the packet loss rate
	rtts.sort()
	totaltimes=len(rtts)
	print 'minimum rtt=',rtts[0]
	print 'maximum rtt=',rtts[totaltimes-1]
	total=0
	for rtt in rtts:
		total=total+rtt
	print 'average RTTs=', (decimal.Decimal(total)/decimal.Decimal(totaltimes))
	print "packet loss rate=%f%%" % (((decimal.Decimal(PINGTIMES)-decimal.Decimal(totaltimes))/decimal.Decimal(PINGTIMES))*100)
	
def udpClientFunc():
	mess=raw_input('what\'s your data?\n')
	for i in range(1,PINGTIMES+1):
		start = datetime.datetime.now()
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		clientSocket.settimeout(1) # time out 1 seconds for blocking method
		clientSocket.sendto(mess,(HOST,PORT))
		try:
			modifiedMessage,(serverAddress,w) = clientSocket.recvfrom(2048)
			printClientInfo(modifiedMessage,serverAddress,start)
		except socket.timeout:
			print 'Request time out'
		except socket.error:
			print 'remote server error'
		clientSocket.close()
		time.sleep(2)
	stats()

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
			printClientInfo(modifiedMessage,serverAddress,start)
		except socket.timeout:
			print 'Request time out'
		except socket.error:
			print 'remote server error'
		clientSocket.close()
		time.sleep(2)
	stats()


if __name__ == '__main__':
	udpClientFunc()
	# tcpClientFunc()