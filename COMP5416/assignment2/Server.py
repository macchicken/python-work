import sys, socket

import RtpPacket
import VideoStream
# from ServerWorker import ServerWorker

class Server:	
	
	def main(self):
		try:
			SERVER_PORT = int(sys.argv[1])
		except:
			print "[Usage: Server.py Server_port]\n"
		rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rtspSocket.bind(('', SERVER_PORT))
		rtspSocket.listen(5)        

		# Receive client info (address,port) through RTSP/TCP session
		while True:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()
			ServerWorker(clientInfo).run()		

class ServerWorker:

	def __init__(self,clientInfo):
		self.clientInfo=clientInfo
		
	def run(self):
		try:
			conn, (address,port)=clientInfo['rtspSocket']
			vFileName,(clientAddress,w) = conn.recvfrom(4096)
			vst=VideoStream(vFileName);data=vst.nextFrame()
			while data!=None:
				rtpp=RtpPacket()
				rtpp.encode(2,0,0,0,vst.frameNbr(),0,26,0,data)
				conn.sendto(rtpp.getPacket(),(address,port))
				data=vst.nextFrame()
		except socket.error:
			print 'receive error'


if __name__ == "__main__":
	(Server()).main()


