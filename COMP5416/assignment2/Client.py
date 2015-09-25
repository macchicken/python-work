import ttk,Tkinter,tkMessageBox,socket,threading,sys,traceback
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
		
	def createWidgets(self):
		mainframe=ttk.Frame(self.master, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		labelframe=ttk.Frame(mainframe, padding="3 3 12 12",height=200)
		labelframe.grid(column=0, row=0, sticky=(N, W, E, S))
		labelframe.columnconfigure(0, weight=1)
		labelframe.rowconfigure(0, weight=1)
		
		self.setup=ttk.Button(mainframe, text="Setup", width=20,command=self.setupMovie)
		self.setup.grid(column=0, row=1, sticky=E,padx=2, pady=2)
		self.play=ttk.Button(mainframe, text="Play", width=20,command=self.playMovie)
		self.play.grid(column=1, row=1, sticky=E,padx=2, pady=2)
		self.pause=ttk.Button(mainframe, text="Pause", width=20,command=self.pauseMovie)
		self.pause.grid(column=2, row=1, sticky=E,padx=2, pady=2)
		self.close=ttk.Button(mainframe, text="Teardown", width=20,command=self.teardown)
		self.close.grid(column=3, row=1, sticky=E,padx=2, pady=2)
		self.label=ttk.Label(labelframe)
		self.label.grid(column=1, row=0, columnspan=4,sticky=W+E+N+S,padx=5, pady=5)
		
	def setupMovie(self):
		if self.state==Cstate.INIT or self.state==Cstate.CONNECTERROR:
			# printLogToConsole("connect to remote stream server")
			try:
				# printLogToConsole("setup moive")
				if self.rtspSocket is None:
					self.rtspSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)# use TCP for rtsp packets
					self.rtspSocket.connect((self.serverAddr, self.serverPort))
				self.seqNumber=self.seqNumber+1
				request=ActionEvents.EVSTEPUP+": "+self.fileName+' '+RTSPVERSION
				request+="\nCSeq: "+str(self.seqNumber)
				request+="\nTransport: %s;client_port= %d" % (RTPTRANSPORT,self.rtpPort)
				self.rtspSocket.send(request)
				self.event=ActionEvents.SETUP
				printLogToConsole(request)
				threading.Thread(target=self.recvRtspReply).start()
			except:
				self.state=Cstate.CONNECTERROR
				self.event=ActionEvents.TEARDOWN
				tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
		
		
	def playMovie(self):
		if self.state==Cstate.READY:
			if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR:
				try:
					# printLogToConsole("play moive")
					self.seqNumber=self.seqNumber+1
					request=ActionEvents.EVPLAY+": "+self.fileName+' '+RTSPVERSION
					request+="\nCSeq: "+str(self.seqNumber)
					request+="\nSession: "+ self.sessionId
					self.rtspSocket.send(request)
					self.event=ActionEvents.PLAY
					printLogToConsole(request)
				except:
					printLogToConsole("play movie error "+str(sys.exc_info()[1]))

	def pauseMovie(self):
		if self.state==Cstate.PLAYING:
			if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR:
				try:
					# printLogToConsole("pause moive")
					self.seqNumber=self.seqNumber+1
					request=ActionEvents.EVPAUSE+": "+self.fileName+' '+RTSPVERSION
					request+="\nCSeq: "+ str(self.seqNumber)
					request+="\nSession: "+ self.sessionId
					self.rtspSocket.send(request)
					self.event=ActionEvents.PAUSE
					printLogToConsole(request)
				except:
					printLogToConsole("pause movie erro "+str(sys.exc_info()[1]))

	def teardown(self):
		if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR and (self.state==Cstate.PLAYING or self.state==Cstate.READY):
			try:
				# printLogToConsole("tear down")
				self.seqNumber=self.seqNumber+1
				request=ActionEvents.EVTEARDOWN+": "+self.fileName+' '+RTSPVERSION
				request+="\nCSeq: "+ str(self.seqNumber)
				request+="\nSession: "+ self.sessionId
				self.rtspSocket.send(request)
				self.event=ActionEvents.TEARDOWN
				printLogToConsole(request)
			except:
				printLogToConsole("tear down error "+str(sys.exc_info()[1]))

	def exitClient(self):
		self.pauseMovie()
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.teardown()
			self.master.destroy()
		else:
			self.playMovie()

	def recvRtspReply(self):
		while True:
			reply=self.rtspSocket.recv(RTSPBUFFERSIZE)
			if reply:
				self.parseRtspReply(reply)
			if self.event == ActionEvents.TEARDOWN:
				break

	def parseRtspReply(self,replyData):
		printLogToConsole(replyData)
		temp=replyData.strip().split("\n")
		self.sessionId=temp[2].split()[1]
		replyCode=temp[0].split(' ',1)[1]
		if replyCode==RESPONSE_OK:
			if self.event==ActionEvents.SETUP:
				self.state=Cstate.READY
			elif self.event==ActionEvents.PLAY:
				try:
					if self.rtpSocket is None:
						self.rtpSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# use UDP for rtp packets
						self.rtpSocket.bind(('', self.rtpPort))# listen for receiving rtp packets
					self.playthread=threading.Event()
					self.playthread.clear()
					self.state=Cstate.PLAYING
					threading.Thread(target=self.parseReplyRtp).start()
				except:
					printLogToConsole("start play thread error "+str(sys.exc_info()[1]))
			elif self.event==ActionEvents.PAUSE:
				self.playthread.set()
				self.state=Cstate.READY
			elif self.event==ActionEvents.TEARDOWN:
				self.playthread.set()
				self.state=Cstate.INIT
				self.seqNumber=0

	def parseReplyRtp(self):
		while True:
			if self.playthread.isSet(): break
			try:
				rtpPacket=self.rtpSocket.recv(RTPBUFFERSIZE)
				if rtpPacket:
					rtpp=RtpPacket()
					rtpp.decode(rtpPacket)
					movieFile="cache-"+self.sessionId+".jpg"
					tmp=open(movieFile,"wb")# write binary
					tmp.write(rtpp.getPayload())# write actual data
					tmp.close()# close to commit to the file
					self.label['image']=ImageTk.PhotoImage(Image.open(movieFile))
			except:
				print "\n"
				traceback.print_exc(file=sys.stdout)