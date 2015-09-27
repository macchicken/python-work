import sys,threading,socket,time,traceback
from random import randint
from VideoStream import VideoStream
from RtpPacket import RtpPacket
from RTPConstants import *
from MyTools import *

class ServerWorker:

	def __init__(self,clientInfo):
		self.clientInfo=clientInfo
		self.csession=0
		self.videoStream=None
		self.rtpPort=None
		self.rtpSocket=None
		self.sendRtpThread=None
		self.clientAddr=None

	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		responseCode=RESPONSE_OK
		while True:
			try:
				conn,(address,port)=self.clientInfo['rtspSocket']
				data,tail=conn.recvfrom(RTSPBUFFERSIZE)
				if data:
					printLogToConsole(data)
					temp=data.split("\n")
					eventType=self.getEventTypeFromRTSP(temp)
					if eventType==ActionEvents.EVSTEPUP:
						self.csession=randint(100000, 999999)
						try:
							self.videoStream=VideoStream(self.getVidoeFileNameFromRTSP(temp))
							self.rtpPort=self.getRtpPortFromRTSP(temp)
							self.clientAddr=address
						except IOError:
							responseCode=RESPONSE_NOTFOUND
					elif eventType==ActionEvents.EVPLAY:
						if self.rtpSocket is None:
							self.rtpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						self.sendRtpThread=threading.Event()
						self.sendRtpThread.clear()
						threading.Thread(target=self.sendRtp).start()
					elif eventType==ActionEvents.EVPAUSE:
						self.sendRtpThread.set()# signal to stop the thread
					elif eventType==ActionEvents.EVTEARDOWN:
						self.sendRtpThread.set()
					conn.send(RTSPVERSION+' '+responseCode+"\n"+temp[1]+"\nSession: "+str(self.csession))
			except socket.error:
				print "\n"
				traceback.print_exc(file=sys.stdout)
			except:
				print "\n"
				traceback.print_exc(file=sys.stdout)

	def getEventTypeFromRTSP(self,request):
		dataFrame=request[0].split()
		return dataFrame[0][:len(dataFrame[0])-1]
	
	def getVidoeFileNameFromRTSP(self,request):
		fileName=request[0].split()[1]
		return fileName
		
	def getRtpPortFromRTSP(self,request):
		dataFrame=request[2].split(';')
		return int(dataFrame[1].split()[1])

	def sendRtp(self):
		while True:
			if self.sendRtpThread.isSet(): break
			time.sleep(0.05)# pause for 50 milliseconds
			try:
				vidata=self.videoStream.nextFrame()
				if vidata:
					rtpp=RtpPacket()
					rtpp.encode(2,0,0,0,self.videoStream.frameNbr(),0,26,6,vidata)
					self.rtpSocket.sendto(rtpp.getPacket(),(self.clientAddr,self.rtpPort))
				else:
					self.sendRtpThread.set()
					break
			except:
				print "\n"
				traceback.print_exc(file=sys.stdout)
