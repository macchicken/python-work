import socket
import threading
from random import randint
from VideoStream import VideoStream
from RtpPacket import RtpPacket
from RTPConstants import *
from MyTools import *

class ServerWorker:

	def __init__(self,clientInfo):
		self.clientInfo=clientInfo
		self.csession=0

	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		while True:
			try:
				conn,(address,port)=self.clientInfo['rtspSocket']
				data,tail = conn.recvfrom(RTSPBUFFERSIZE)
				if data:
					pringLogToConsole("Data received: "+data)
					temp=data.split("\n")
					eventType=self.getEventTypeFromRTSP(temp)
					if eventType==ActionEvents.EVSTEPUP:
						self.csession=randint(100000, 999999)
					conn.send(RTSPVERSION+" 200 OK\n"+temp[1]+"\nSession: "+str(self.csession))
			except socket.error:
				print pringLogToConsole("receive error")

	def getEventTypeFromRTSP(self,request):
		dataFrame=request[0].split()
		return dataFrame[0][:len(dataFrame[0])-1]
		
	# def recvRtspRequest(self):
		# while True:
			# try:
			# conn,(address,port)=clientInfo['rtspSocket']
			# vFileName,(clientAddress,w) = conn.recvfrom(RTSPBUFFERSIZE)
			# vst=VideoStream(vFileName);data=vst.nextFrame()
			# while data!=None:
				# rtpp=RtpPacket()
				# rtpp.encode(2,0,0,0,vst.frameNbr(),0,26,0,data)
				# conn.sendto(rtpp.getPacket(),(address,port))
				# data=vst.nextFrame()
		# except socket.error:
			# print 'receive error'