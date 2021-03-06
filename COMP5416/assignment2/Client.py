from Tkinter import *
import tkMessageBox,socket,threading,sys,traceback,time,datetime
from PIL import Image,ImageTk
from RTPConstants import *
from MyTools import *
from RtpPacket import RtpPacket


class Client:
	
	def __init__(self,tkRoot,serverAddr,serverPort,rtpPort,fileName):
		self.master=tkRoot
		self.master.protocol("WM_DELETE_WINDOW", self.exitClient)
		self.serverAddr=serverAddr
		self.serverPort=int(serverPort)
		self.rtpPort=int(rtpPort)
		self.fileName=fileName
		self.createWidgets()
		self.seqNumber=0
		self.state=Cstate.INIT
		self.event=ActionEvents.TEARDOWN
		self.sessionId="0"
		self.rtspSocket=None
		self.rtpSocket=None
		self.playthread=None
		self.videoSize=0
		self.loadedFrame=[]
		self.playTimeElapsed=0
		self.playStartTime=0
		self.totalFrame="0"
		self.frameNumber=0
		self.endOfStream=False
		self.fileWritelock=threading.Lock()


	def createWidgets(self):
		self.setup=Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Setup"
		self.setup["command"] = self.setupMovie
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		self.play=Button(self.master, width=20, padx=3, pady=3)
		self.play["text"] = "Play"
		self.play["command"] = self.playMovie
		self.play.grid(row=1, column=1, padx=2, pady=2)
		
		self.pause=Button(self.master, width=20, padx=3, pady=3)
		self.pause["text"] = "Pause"
		self.pause["command"] = self.pauseMovie
		self.pause.grid(row=1, column=2, padx=2, pady=2)
		
		self.close=Button(self.master, width=20, padx=3, pady=3)
		self.close["text"] = "Teardown"
		self.close["command"] = self.teardown
		self.close.grid(row=1, column=3, padx=2, pady=2)
		
		self.label=Label(self.master, height=19)
		self.label.grid(row=0, column=0, columnspan=5, sticky=W+E+N+S, padx=5, pady=5)

		
	def setupMovie(self):
		if self.state==Cstate.INIT or self.state==Cstate.CONNECTERROR:
			# printLogToConsole("connect to remote stream server")
			try:
				# printLogToConsole("setup moive")
				if self.rtspSocket is None:
					self.rtspSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# use TCP for rtsp packets
					self.rtspSocket.connect((self.serverAddr, self.serverPort))
				threading.Thread(target=self.recvRtspReply).start()
				self.seqNumber=self.seqNumber+1
				request=ActionEvents.EVSTEPUP+": "+self.fileName+' '+RTSPVERSION
				request+=MESSAGESEP+"CSeq: "+str(self.seqNumber)
				request+=MESSAGESEP+"Transport: %s;client_port= %d" % (RTPTRANSPORT,self.rtpPort)
				self.rtspSocket.send(request)
				self.event=ActionEvents.SETUP
				printLogToConsole(request)
			except:
				self.state=Cstate.CONNECTERROR
				self.event=ActionEvents.TEARDOWN
				tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
		
		
	def playMovie(self):
		if self.state==Cstate.READY:
			if self.rtspSocket is not None:
				try:
					# printLogToConsole("play moive")
					self.seqNumber=self.seqNumber+1
					request=self.constructReq(ActionEvents.EVPLAY)
					self.rtspSocket.send(request)
					self.event=ActionEvents.PLAY
					printLogToConsole(request)
					if self.playStartTime==0: self.playStartTime=datetime.datetime.now()
					try:
						if self.rtpSocket is None:
							self.rtpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# use UDP for rtp packets
							self.rtpSocket.bind(('', self.rtpPort))# listen for receiving rtp packets
						self.playthread=threading.Event()
						self.playthread.clear()
						threading.Thread(target=self.parseReplyRtp).start()
					except:
						printLogToConsole("start play thread error "+str(sys.exc_info()[1]))
				except:
					printLogToConsole("play movie error "+str(sys.exc_info()[1]))


	def pauseMovie(self):
		if self.state==Cstate.PLAYING:
			if self.rtspSocket is not None:
				try:
					# printLogToConsole("pause moive")
					self.seqNumber=self.seqNumber+1
					request=self.constructReq(ActionEvents.EVPAUSE)
					self.rtspSocket.send(request)
					self.event=ActionEvents.PAUSE
					printLogToConsole(request)
					self.calculateTimeDiff()
				except:
					printLogToConsole("pause movie erro "+str(sys.exc_info()[1]))


	def teardown(self):
		if self.rtspSocket is not None and (self.state==Cstate.PLAYING or self.state==Cstate.READY):
			try:
				# printLogToConsole("tear down")
				self.seqNumber=self.seqNumber+1
				request=self.constructReq(ActionEvents.EVTEARDOWN)
				self.rtspSocket.send(request)
				self.event=ActionEvents.TEARDOWN
				printLogToConsole(request)
				if not self.endOfStream:
					self.calculateTimeDiff()
					self.endOfStream=True
			except:
				printLogToConsole("tear down error "+str(sys.exc_info()[1]))


	def exitClient(self):
		self.pauseMovie()
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.teardown()
			if self.rtspSocket is not None:
				self.seqNumber=self.seqNumber+1
				request=self.constructReq(ActionEvents.EVCLOSERTSPSOCKET)
				self.rtspSocket.send(request)
				self.rtspSocket.close()
			self.master.destroy()
		else:
			self.playMovie()


	def recvRtspReply(self):
		while True:
			reply=self.rtspSocket.recv(RTSPBUFFERSIZE)
			if reply:
				self.parseRtspReply(reply)
			if self.event == ActionEvents.TEARDOWN: break


	def parseRtspReply(self,replyData):
		printLogToConsole(replyData)
		temp=replyData.strip().split(MESSAGESEP)
		replyCode=temp[0].split(' ',1)[1]
		if replyCode==RESPONSE_OK:
			if self.event==ActionEvents.SETUP:
				self.state=Cstate.READY
				self.sessionId=temp[2].split()[1]
				self.videoSize=temp[3].split()[1]
			if self.sessionId==temp[2].split()[1]:
				if self.event==ActionEvents.PLAY:
					self.state=Cstate.PLAYING
				elif self.event==ActionEvents.PAUSE:
					self.playthread.set()
					self.state=Cstate.READY
				elif self.event==ActionEvents.TEARDOWN:
					self.playthread.set()
					self.state=Cstate.INIT
					self.printStats()
					self.seqNumber=0
					self.videoSize=0
					self.playTimeElapsed=0
					self.loadedFrame=[]
					self.totalFrame="0"
					self.playStartTime=0
					self.sessionId="0"
					self.frameNumber=0
					self.endOfStream=False
					print "back to init"
		elif replyCode==RESPONSE_NOTFOUND:
			self.state=Cstate.INIT
			self.seqNumber=0


	def parseReplyRtp(self):
		while True:
			if self.playthread.isSet(): break
			try:
				rtpPacket=self.rtpSocket.recv(RTPBUFFERSIZE)
				if rtpPacket:
					if not rtpPacket.startswith(RTSPVERSION):
						self.fileWritelock.acquire()# acquire lock for writing image file to the disk
						try:
							rtpp=RtpPacket()
							rtpp.decode(rtpPacket)
							if self.frameNumber<rtpp.seqNum():# ignore late packets with lower sequence number
								self.frameNumber=rtpp.seqNum()
								movieFile="cache-"+self.sessionId+".jpg"
								with open(movieFile,"wb") as tmp:# write binary
									tmp.write(rtpp.getPayload())# write actual data
								self.loadedFrame.append(rtpp)
								time.sleep(0.05)# pause for 50 milliseconds for synchronized with server sending interval
								photo=ImageTk.PhotoImage(Image.open(movieFile))
								self.label.configure(image=photo,height=288)
								self.label.image=photo
						finally:
							self.fileWritelock.release()# release the lock
					else:
						print rtpPacket
						self.endOfStream=True
						temp=rtpPacket.strip().split(MESSAGESEP)
						self.calculateTimeDiff()
						self.totalFrame=temp[1].split()[1]
			except:
				print "\n"
				traceback.print_exc(file=sys.stdout)


	def printStats(self):
		print "video size: %s bytes, time elapsed: %d seconds" % (self.videoSize,int(self.playTimeElapsed))
		if self.totalFrame!="0":
			frameCount=len(self.loadedFrame)
			print "client frame count: %s, total frame from server: %s" % (str(frameCount),self.totalFrame)
			totalBytes=0
			for rttp in self.loadedFrame:
				totalBytes+=len(rttp.getPayload())
			print "transfer rate: %f bit/s" % (totalBytes*8/self.playTimeElapsed)
			print "packet loss rate: %f" % (((int(self.totalFrame)-frameCount)*1.0/int(self.totalFrame))*100)


	def calculateTimeDiff(self):
		stTime=datetime.datetime.now()
		self.playTimeElapsed=self.playTimeElapsed+((stTime-self.playStartTime).total_seconds())
		self.playStartTime=stTime
		
	def constructReq(self,actionEv):
		request=actionEv+": "+self.fileName+' '+RTSPVERSION
		request+=MESSAGESEP+"CSeq: "+ str(self.seqNumber)
		request+=MESSAGESEP+"Session: "+ self.sessionId
		return request