import os
import time


class ImgbinData:
	
	def __init__(self,imgLen,rawData):
		self.imgLen=imgLen
		self.rawData=rawData
	
	def getImgLen(self):
		return self.imgLen
	
	def getRawData(self):
		return self.rawData


def appendZeroToFive(str):
	if len(str)>=5: return str
	else: return appendZeroToFive('0'+str)

def toMjpeg(dirName="D:\\workspace\\python-work\\COMP5416\\assignment2\\test"):
	waitingData=[]
	for fileName in os.listdir(dirName):
		with open(dirName+"\\"+fileName,"rb") as jpgfile:
			data=jpgfile.read()
			imglen=appendZeroToFive(str(os.path.getsize(dirName+"\\"+fileName)))
			temp=ImgbinData(imglen,data)
			waitingData.append(temp)
	time.sleep(3)
	with open (dirName+"\\"+"result.Mjpeg","wb") as mjpegFile: 
		for tdata in waitingData:
			mjpegFile.write(tdata.getImgLen())
			print "write file length %s" % tdata.getImgLen()
			time.sleep(3)
			mjpegFile.write(tdata.getRawData())
			print "write image bin data"
			time.sleep(3)
			
			
if __name__ == '__main__':
	toMjpeg()