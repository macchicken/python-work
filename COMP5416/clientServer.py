import socket
import datetime
import time

class ClientServer(object):
	
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
		elif self.mode==2:
			for i in range(1,self.pingtimes+1):
				start = datetime.datetime.now()
				clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
				clientSocket.settimeout(1) # time out 1 seconds for blocking method
				try:
					clientSocket.connect((self.host, self.port))
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
				
	def serverStartup(self):
		if self.mode==1:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			s.bind((self.host, self.port))
			while True:
				message, clientAddress = s.recvfrom(2048)
				if not message: continue
				print 'Connected by ', clientAddress
				print 'message ', message
				message=message.upper()+" modified by server"
				s.sendto(message,clientAddress)
			s.close()
		elif self.mode==2:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
			s.bind((self.host, self.port))
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