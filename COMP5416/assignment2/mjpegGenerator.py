import os
import time

myseparator=os.sep

class ImgbinData:
	
	def __init__(self,imgLen,rawData,fileName):
		self.imgLen=imgLen
		self.rawData=rawData
		self.fileName=fileName
	
	def getImgLen(self):
		return self.imgLen
	
	def getRawData(self):
		return self.rawData
		
	def getFileName(self):
		return self.fileName
		
	def __repr__(self):
		return self.fileName

# file name must be numbers
def ImgbinDataCmp(imgb1,imgb2):
	b1=int(imgb1.fileName.split('.')[0])
	b2=int(imgb2.fileName.split('.')[0])
	if b1<b2: return -1
	elif b1==b2: return 0
	else: return 1
	
def appendZeroToFive(str):
	if len(str)>=5: return str
	else: return appendZeroToFive('0'+str)

def toMjpeg(dirName="Converted"):
	waitingData=[]
	for fileName in os.listdir(dirName):
		with open(dirName+myseparator+fileName,"rb") as jpgfile:
			data=jpgfile.read()
			imglen=appendZeroToFive(str(os.path.getsize(dirName+myseparator+fileName)))
			temp=ImgbinData(imglen,data,fileName)
			waitingData.append(temp)
	time.sleep(1)
	waitingData.sort(cmp=ImgbinDataCmp)
	time.sleep(1)
	with open (dirName+myseparator+"result-berry.Mjpeg","wb") as mjpegFile: 
		for tdata in waitingData:
			mjpegFile.write(tdata.getImgLen())
			print "write file length %s with file %s" % (tdata.getImgLen(),tdata.getFileName())
			time.sleep(1)
			mjpegFile.write(tdata.getRawData())
			print "write image bin data"
			time.sleep(1)
			
			
if __name__ == '__main__':
	toMjpeg()