import sys,threading,socket,time,traceback,os
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
		self.rtspConn=None
		

	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()


	def recvRtspRequest(self):
		responseCode=RESPONSE_OK
		conn,(address,port)=self.clientInfo['rtspSocket']
		self.rtspConn=conn
		spath=os.path.dirname(os.path.realpath(sys.argv[0]))
		while True:
			try:
				data,tail=conn.recvfrom(RTSPBUFFERSIZE)
				if data:
					printLogToConsole(data)
					temp=data.split("\n")
					eventType=self.getEventTypeFromRTSP(temp)
					otherData=''
					if eventType==ActionEvents.EVSTEPUP:
						self.csession=randint(100000, 999999)
						try:
							vFileName=spath+"\\"+self.getVidoeFileNameFromRTSP(temp)
							self.videoStream=VideoStream(vFileName)
							self.rtpPort=self.getRtpPortFromRTSP(temp)
							self.clientAddr=address
							otherData="\nVsize: "+str(os.stat(vFileName).st_size)
						except IOError:
							responseCode=RESPONSE_NOTFOUND
					elif eventType==ActionEvents.EVPLAY:
						if self.rtpSocket is None:
							self.rtpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						self.sendRtpThread=threading.Event()
						self.sendRtpThread.clear()
						threading.Thread(target=self.sendRtp).start()
					elif eventType==ActionEvents.EVPAUSE:
						if self.sendRtpThread is not None:
							self.sendRtpThread.set()# signal to stop the thread
					elif eventType==ActionEvents.EVTEARDOWN:
						if self.sendRtpThread is not None:
							self.sendRtpThread.set()
					conn.send(RTSPVERSION+' '+responseCode+"\n"+temp[1]+"\nSession: "+str(self.csession)+otherData)
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
					print "end of stream"
					self.sendRtpThread.set()
					self.rtpSocket.sendto(RTSPVERSION+' '+RESPONSE_OK_END+"\nTotalFrame: "+str(self.videoStream.frameNbr())+"\nSession: "+str(self.csession),(self.clientAddr,self.rtpPort))
					try:
						self.videoStream.file.close()
					except: print "close file error"
					break
			except:
				print "\n"
				traceback.print_exc(file=sys.stdout)
