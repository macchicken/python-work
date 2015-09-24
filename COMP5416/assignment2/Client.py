import ttk
import tkMessageBox
import socket
import threading
from RTPConstants import *
from MyTools import *

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
		
	def createWidgets(self):
		mainframe = ttk.Frame(self.master, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		labelframe = ttk.Frame(mainframe, padding="3 3 12 12",height=200)
		labelframe.grid(column=0, row=0, sticky=(N, W, E, S))
		labelframe.columnconfigure(0, weight=1)
		labelframe.rowconfigure(0, weight=1)
		
		self.setup = ttk.Button(mainframe, text="Setup", width=20,command=self.setupMovie).grid(column=0, row=1, sticky=E,padx=2, pady=2)
		self.play = ttk.Button(mainframe, text="Play", width=20,command=self.playMovie).grid(column=1, row=1, sticky=E,padx=2, pady=2)
		self.pause = ttk.Button(mainframe, text="Pause", width=20,command=self.pauseMovie).grid(column=2, row=1, sticky=E,padx=2, pady=2)
		self.close = ttk.Button(mainframe, text="Teardown", width=20,command=self.teardown).grid(column=3, row=1, sticky=E,padx=2, pady=2)
		self.label = ttk.Label(labelframe).grid(column=0, row=0, columnspan=4,sticky=W+E+N+S,padx=5, pady=5)
		
	def setupMovie(self):
		if self.state==Cstate.INIT or self.state==Cstate.CONNECTERROR:
			pringLogToConsole("connect to remote stream server")
			try:
				if self.rtspSocket is None:
					self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# use TCP for rtsp packets
					self.rtspSocket.connect((self.serverAddr, self.serverPort))
					pringLogToConsole("setup moive")
					self.seqNumber=self.seqNumber+1
					request=ActionEvents.EVSTEPUP+": "+self.fileName+' '+RTSPVERSION
					request+="\nCSeq: "+str(self.seqNumber)
					request+="\nTransport: %s;client_port= %d" % (RTPTRANSPORT,self.rtpPort)
					self.rtspSocket.send(request)
					pringLogToConsole(request)
					self.event=ActionEvents.SETUP
					self.state=Cstate.READY
					threading.Thread(target=self.recvRtspReply).start()
			except:
				self.state=Cstate.CONNECTERROR
				self.event=ActionEvents.TEARDOWN
				self.rtspSocket=None
				tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
		
		
	def playMovie(self):
		if self.state==Cstate.READY:
			if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR:
				try:
					pringLogToConsole("play moive")
					self.seqNumber=self.seqNumber+1
					request=ActionEvents.EVPLAY+": "+self.fileName+' '+RTSPVERSION
					request+="\nCSeq: "+str(self.seqNumber)
					request+="\nSession: "+ self.sessionId
					self.rtspSocket.send(request)
					self.event=ActionEvents.PLAY
					self.state=Cstate.PLAYING
					pringLogToConsole(request)
				except:
					pringLogToConsole("play movie error")

	def pauseMovie(self):
		if self.state==Cstate.PLAYING:
			if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR:
				try:
					pringLogToConsole("pause moive")
					self.seqNumber=self.seqNumber+1
					request=ActionEvents.EVPAUSE+": "+self.fileName+' '+RTSPVERSION
					request+="\nCSeq: "+ str(self.seqNumber)
					request+="\nSession: "+ self.sessionId
					self.rtspSocket.send(request)
					self.event=ActionEvents.PAUSE
					self.state=Cstate.READY
					pringLogToConsole(request)
				except:
					pringLogToConsole("pause movie erro")

	def teardown(self):
		if self.rtspSocket is not None and self.state!=Cstate.CONNECTERROR and (self.state==Cstate.PLAYING or self.state==Cstate.READY):
			try:
				pringLogToConsole("tear down")
				self.seqNumber=self.seqNumber+1
				request=ActionEvents.EVTEARDOWN+": "+self.fileName+' '+RTSPVERSION
				request+="\nCSeq: "+ str(self.seqNumber)
				request+="\nSession: "+ self.sessionId
				self.rtspSocket.send(request)
				self.event=ActionEvents.TEARDOWN
				self.state=Cstate.INIT
				self.seqNumber=0
				pringLogToConsole(request)
			except:
				pringLogToConsole("tear down error")

	def exitClient(self):
		self.pauseMovie()
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.teardown()
			self.master.destroy()
		else:
			self.playMovie()

	def recvRtspReply(self):
		while True:
			reply = self.rtspSocket.recv(RTSPBUFFERSIZE)
			if reply:
				self.parseRtspReply(reply)
			if self.event == ActionEvents.TEARDOWN:
				self.rtspSocket.shutdown(socket.SHUT_RDWR)
				self.rtspSocket.close()
				self.rtspSocket=None
				break

	def parseRtspReply(self,replyData):
		pringLogToConsole(replyData)
		temp=replyData.split("\n")
		self.sessionId=temp[2].split()[1]
		