import ttk
import tkMessageBox
import socket
from RTPConstants import *

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
		self.sentRequest=READY
		self.sessionId=0
		self.rtspSocket=None
		
	def createWidgets(self):
		mainframe = ttk.Frame(self.master, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		mainframe.columnconfigure(0, weight=1)
		mainframe.rowconfigure(0, weight=1)
		labelframe = ttk.Frame(mainframe, padding="3 3 12 12",height=200)
		labelframe.grid(column=0, row=0, sticky=(N, W, E, S))
		labelframe.columnconfigure(0, weight=1)
		labelframe.rowconfigure(0, weight=1)
		
		self.setup = ttk.Button(mainframe, text="Init", width=20,command=self.initMovie).grid(column=0, row=1, sticky=E,padx=2, pady=2)
		self.play = ttk.Button(mainframe, text="Play", width=20,command=self.playMovie).grid(column=1, row=1, sticky=E,padx=2, pady=2)
		self.pause = ttk.Button(mainframe, text="Pause", width=20,command=self.pauseMovie).grid(column=2, row=1, sticky=E,padx=2, pady=2)
		self.close = ttk.Button(mainframe, text="Close", width=20,command=self.closeStream).grid(column=3, row=1, sticky=E,padx=2, pady=2)
		self.label = ttk.Label(labelframe).grid(column=0, row=0, columnspan=4,sticky=W+E+N+S,padx=5, pady=5)
		
	def initMovie(self):
		if self.sentRequest==SETUP or self.sentRequest==READY or self.sentRequest==CONNECTERROR:
			print 'connect to remote stream server'
			if self.rtspSocket is not None: self.rtspSocket.close()
			self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				self.rtspSocket.connect((self.serverAddr, self.serverPort))
				print 'setup moive'
				self.seqNumber=self.seqNumber+1
				request='init '+self.fileName+' '+VERSION
				request+="\nSeq: "+str(self.seqNumber)
				request+="\nTransport: %s; client_port= %d" % (TRANSPORT,self.rtpPort)
				self.rtspSocket.send(request)
				self.sentRequest=SETUP
			except:
				self.sentRequest=CONNECTERROR
				tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' %self.serverAddr)
		
		
	def playMovie(self):
		if self.sentRequest==SETUP or self.sentRequest==PAUSE:
			print 'play moive'
			if self.rtspSocket is not None and self.sentRequest!=CONNECTERROR:
				self.seqNumber=self.seqNumber+1
				request='play '+self.fileName+' '+VERSION
				request+="\nSeq: "+str(self.seqNumber)
				request+="\nSession: "+ str(self.sessionId)
				self.rtspSocket.send(request)
				self.sentRequest=PLAY
				print '\nData sent:' + request
	
	def pauseMovie(self):
		if self.sentRequest==PLAY:
			print 'pause moive'
			if self.rtspSocket is not None and self.sentRequest!=CONNECTERROR:
				self.seqNumber=self.seqNumber+1
				request='pause '+self.fileName+' '+VERSION
				request+="\nSeq: "+ str(self.seqNumber)
				request+="\nSession: "+ str(self.sessionId)
				self.rtspSocket.send(request)
				self.sentRequest=PAUSE
				print '\nData sent:' + request
	
	def closeStream(self):
		if self.rtspSocket is not None and self.sentRequest!=CONNECTERROR and self.sentRequest!=CLOSE:
			print 'close stream'
			self.seqNumber=self.seqNumber+1
			request="close "+self.fileName+' '+VERSION
			request+="\nSeq: "+ str(self.seqNumber)
			request+="\nSession: "+ str(self.sessionId)
			self.rtspSocket.send(request)
			self.sentRequest=CLOSE
			print '\nData sent:' + request
	
	def exitClient(self):
		self.pauseMovie()
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.closeStream()
			self.master.destroy()
		else:
			self.playMovie()