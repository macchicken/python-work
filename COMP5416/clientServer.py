import socket
import datetime
import time
import decimal
import random

"""
MODE 1 - UDP
MODE 2 - TCP
"""

class ClientServer(object):
	
	rtts=[]				  # list of rtt of each ping

	def __init__(self,PORT=50007,PINGTIMES=10,HOST='localhost',SERVERHOST='',MODE=1):
		self.port=PORT # The same port as used by the server
		self.pingtimes=PINGTIMES # ping times used in the client
		self.host=HOST
		self.serverhost=SERVERHOST
		self.mode=MODE

	def clientConnect(self):
		mess=raw_input('what\'s your data?\n')
		if self.mode==1:
			for i in range(1,self.pingtimes+1):
				start = datetime.datetime.now()
				clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
				clientSocket.settimeout(1) # time out 1 seconds for blocking method
				clientSocket.sendto(mess,(self.host,self.port))
				try:
					modifiedMessage,(serverAddress,w) = clientSocket.recvfrom(2048)
					self.__printClientInfo(modifiedMessage,serverAddress,start)
				except socket.timeout:
					print 'Request time out'
				except socket.error:
					print 'remote server error'
				clientSocket.close()
				time.sleep(2)
		elif self.mode==2:
			for i in range(1,self.pingtimes+1):
				start = datetime.datetime.now()
				clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
				clientSocket.settimeout(1) # time out 1 seconds for blocking method
				try:
					clientSocket.connect((self.host, self.port))
					clientSocket.sendall(mess)
					modifiedMessage,(serverAddress,w) = clientSocket.recvfrom(2048)
					self.__printClientInfo(modifiedMessage,serverAddress,start)
				except socket.timeout:
					print 'Request time out'
				except socket.error:
					print 'remote server error'
				clientSocket.close()
				time.sleep(2)
		self.__stats()

	def serverStartup(self):
		if self.mode==1:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			s.bind((self.serverhost, self.port))
			while True:
				rand=random.randint(0, 10)
				try:
					message, clientAddress = s.recvfrom(2048)
					if not message: continue
				except socket.error:
					print 'receive error'
					continue
				self.__printServerInfo(message, clientAddress)
				message=message.upper()
				if rand<4: continue # If rand is less is than 4, we consider the packet lost and do not respond
				s.sendto(message,clientAddress)
			s.close()
		elif self.mode==2:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
			s.bind((self.serverhost, self.port))
			s.listen(5)
			conn, addr = s.accept()
			while True:
				rand=random.randint(0, 10)
				try:
					message, (w,clientAddress) = conn.recvfrom(2048)
					if not message: conn.close();conn, addr = s.accept();continue
				except socket.error:
					print 'receive error'
					continue
				self.__printServerInfo(message, addr)
				message=message.upper()
				if rand<4: continue # If rand is less is than 4, we consider the packet lost and do not respond
				conn.sendall(message)
			conn.close()
	
	def __printClientInfo(self,modifiedMessage,serverAddress,startTime): # print information of client at each ping
		print 'server address=', serverAddress
		print 'Received=', repr(modifiedMessage)
		end = datetime.datetime.now()
		interval=end-startTime
		rtt=int(interval.total_seconds()*1000)
		print 'round trip time=',rtt
		self.rtts.append(rtt)

	def __printServerInfo(self,message,clientAddress): # print information of server at each ping packet receive
		print 'Connected by ', clientAddress, 'at ', datetime.datetime.now()
		print 'Received message ', message
		
	def __stats(self): # report the packet loss rate
		self.rtts.sort()
		totaltimes=len(self.rtts)
		print 'minimum rtt=',self.rtts[0]
		print 'maximum rtt=',self.rtts[totaltimes-1]
		total=0
		for rtt in self.rtts:
			total=total+rtt
		print 'average RTTs=', (decimal.Decimal(total)/decimal.Decimal(totaltimes))
		print "packet loss rate=%f%%" % (((decimal.Decimal(self.pingtimes)-decimal.Decimal(totaltimes))/decimal.Decimal(self.pingtimes))*100)