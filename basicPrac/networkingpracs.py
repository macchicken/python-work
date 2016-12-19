"""
typical http response headers:
[('content-length', '14'), ('set-cookie', 'JSESSIONID=B381255CC79055907189BF931802DC6A;Path=/qmoon'),
('x-via', '1.1 gm249:80 (Cdn Cache Server V2.0), 1.1 gzqxg206:8085 (Cdn Cache Server V2.0)'),
('connection', 'keep-alive'), ('date', 'Fri, 07 Jun 2013 04:09:10 GMT'),
('content-type', 'text/html;charset=UTF-8')]
or
[('x-via', '1.1 gm249:80 (Cdn Cache Server V2.0), 1.1 gzqxg206:8085 (Cdn Cache Server V2.0)'),
('content-disposition', 'attachment;filename=news_pic.gif'), ('transfer-encoding', 'chunked'),
('connection', 'keep-alive'), ('date', 'Fri, 07 Jun 2013 04:27:11 GMT'),
('content-type', 'application/octet-stream')]
"""

from httplib import HTTPConnection
import socket,json,os
from ssl import wrap_socket
from pprint import pformat
from urllib2 import urlopen
from urllib2 import HTTPError
from sys import exc_info
from Queue import Queue
from threading import Thread
from argparse import ArgumentParser
from bs4 import BeautifulSoup

SUFFIXS=['gif','jpg','jpeg','png','bmp','mp3','wav','wma','doc']
urlQ=Queue()
if not os.path.isdir("downloaddirc"): os.mkdir("downloaddirc")

def c(sequence):
	for item in sequence:
		c.items+=1
		yield item

def transferSuffix(content_disposition):
	try:
		filename=content_disposition.rsplit('filename=')[1].split('.')
		suffix=filename[len(filename)-1]
		return next((supportSuffix for supportSuffix in SUFFIXS
					 if suffix==supportSuffix))
	except StopIteration:
		return None

def connectHttpFromDomain(domainName,requestUrl,id):
	print "ID",id
	conn = HTTPConnection(domainName)
	conn.request("GET", requestUrl)
	r1 = conn.getresponse()
	content_type=r1.getheader('content-type')
	content_disposition=r1.getheader('content-disposition')
	reason=r1.reason
	status=r1.status
	# print status, reason
	data = r1.read() #whole response data
	conn.close()
	return data,status,reason,content_type,content_disposition

def connectSSl(requestUrl,port=443):
	ssl_sock=None
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssl_sock = wrap_socket(s)
		ssl_sock.connect((requestUrl, port))
		print repr(ssl_sock.getpeername())
		print ssl_sock.cipher()
		print pformat(ssl_sock.getpeercert())
		ssl_sock.write("GET / HTTPS/1.0\rHost:www.udacity.com\r\n\r\n")
		data = ssl_sock.read()
		print data
		ssl_sock.close()
	except socket.error:
		print exc_info()
	finally:ssl_sock.close()
		
def saveFileFromStream(data,id,content_disposition,error_data):
	if content_disposition is not None:
		suffix=transferSuffix(content_disposition)
		if suffix is not None:
			try:
				target = open("testImg\\911Pop_"+str(id)+'.'+suffix, "wb")#open in binary write mode
				target.write(data)
				target.close()
			except BaseException:
				error_data.append(str(id)+':'+str(len(data)))
			pass
		else:
			print "not spporting type",id,content_disposition
			error_data.append(str(id)+':'+str(len(data))+':'+'not spporting type')

def downloadFilebyUrl(requestUrl,FileName):
	print 'downloading '+requestUrl
	try:
		conn = urlopen(requestUrl)
		target = open("downloaddirc\\"+FileName, "wb")
		target.write(conn.read())
		conn.close()
		target.close()
	except HTTPError:
		print 'HTTPError on',requestUrl
		c.items-=1

def downloadFileWorker():
	while True:
		requestUrl=urlQ.get(block=True)
		downloadFilebyUrl(requestUrl,os.path.basename(requestUrl).replace('\n',''))
		urlQ.task_done()

def parseYahooPicVarData():
	target = open("yahooPicData.txt", "r")
	requestUrlList=[]
	for element in target.read().split(','):
		if 'src' in element:
			url_text=(element.replace('"src":"','')).replace('"}','')
			if 'original' in url_text:
				requestUrlList.append(url_text.replace('\\',''))
	target.close()
	return requestUrlList

def downloadYahooPicData():
	requestUrlList=parseYahooPicVarData()
	c.items=0
	for requestUrl in c(requestUrlList):
		# urlItems=requestUrl.split('/')
		# downloadFilebyUrl(requestUrl,urlItems[-1])
		downloadFilebyUrl(requestUrl,os.path.basename(requestUrl))
	print '%d file downloaded' % (c.items)


# galleryDataUrl  /photoview/00AJ0003/620366.html
def download163galleryData(mutiltask=False):
	with open("neteaseData.txt","rb") as tempRead:
		for line in tempRead:
			galleryDataUrl=line.strip("\n|' '").split("/",1)
			data,status,reason,content_type,content_disposition=connectHttpFromDomain(galleryDataUrl[0],"/"+galleryDataUrl[1],"-1")
			if status==200 and reason=='OK':
				pageData=BeautifulSoup(data,'html.parser')
				galleryData=pageData.find("textarea",attrs={"name": "gallery-data"})
				jData=json.loads(galleryData.contents[0].strip())
				imgList=jData["list"]
				c.items=0
				for imgObj in c(imgList):
					imgUrl=imgObj["oimg"].strip("\n|' '")
					if mutiltask:
						urlQ.put(imgUrl)
					else:
						downloadFilebyUrl(imgUrl,os.path.basename(imgUrl))
				if mutiltask:
					for i in range(10):
						t=Thread(target=downloadFileWorker)
						t.daemon=True
						t.start()
					urlQ.join()
				print '%d file downloaded' % (c.items)

def download911PopData():
	error_data=[]
	domainName='www.911pop.com'
	requestUrl='/qmoon/Preview/qmyl/CatalogResources.frontDownload.zaction?ID='
	for i in range(1,4490):
		data,status,reason,content_type,content_disposition=connectHttpFromDomain(domainName,requestUrl+str(i),i)
		if status==200 and reason=='OK' and "text/html" not in content_type:
			saveFileFromStream(data,i,content_disposition,error_data)
	try:
		error_result=open("error_result.txt","w")
		for item in error_data:
			error_result.write(str(item)+'\n')
		error_result.close()
	except IOError:
		print "error occur during writing error result"

def downloadMsnPicData():
	with open("msnPicData.txt","r") as target:
		c.items=0
		for line in c(target):
			# urlItems=line.split('/')
			# downloadFilebyUrl(line,urlItems[-1].replace('\n',''))
			downloadFilebyUrl(line,os.path.basename(line).replace('\n',''))
	if not target.closed:
		print 'closing'
		target.close()
	print '%d file downloaded' % (c.items)

def downloadEntqqData():
	with open("netqqData.txt","rb") as tempRead:
		for line in tempRead:
			galleryDataUrl=line.strip("\n|' '").split("/",1)
			data,status,reason,content_type,content_disposition=connectHttpFromDomain(galleryDataUrl[0],"/"+galleryDataUrl[1],"-1")
			if status==200 and reason=='OK':
				pageData=BeautifulSoup(data,'html.parser')
				alternateUrl=pageData.find("link",attrs={"rel":"alternate"})["href"].replace("http://",'').split("/",1)
				adata,astatus,areason,acontent_type,acontent_disposition=connectHttpFromDomain(alternateUrl[0],"/"+alternateUrl[1],"0")
				if astatus==200 and areason=='OK':
					apageData=BeautifulSoup(adata,'html.parser')
					contentFontsmall=apageData.find("div",attrs={"class":"content fontsmall"})
					imageSplits=contentFontsmall.find_all("div",attrs={"class":"image split"})
					c.items=0
					for oneImage in c(imageSplits):
						realImage=oneImage.select("img")[0]["src"]
						downloadFilebyUrl(realImage,realImage.split("/")[-2:][0]+".jpg")
					print '%d file downloaded' % (c.items)

def main():
	cmdparse=ArgumentParser(description='download image files from url file')
	group=cmdparse.add_mutually_exclusive_group()
	group.add_argument('-n','--netease',dest='netease',default=False,action='store_true',help="download 163 web pics")
	group.add_argument('-m','--msn',dest='msn',default=False,action='store_true',help="download msn web pics")
	group.add_argument('-y','--yahoo',dest='yahoo',default=False,action='store_true',help="download yahoo web pics")
	group.add_argument('-911','--911pop',dest='pop',default=False,action='store_true',help="download 911pop web pics")
	group.add_argument('-eq','--entqq',dest='entqq',default=False,action='store_true',help="download ent qq web pics")
	args=cmdparse.parse_args()
	if args.netease: download163galleryData(mutiltask=True)
	elif args.msn: downloadMsnPicData()
	elif args.yahoo: downloadYahooPicData()
	elif args.pop: download911PopData()
	elif args.entqq: downloadEntqqData()
	else: print 'at least one argument,type -h for help messages'

if __name__ == '__main__':
	# print transferSuffix('attachment;ttttfilename=news_pic.JPG.jpg')
	# connectSSl('www.youtube.com')
	# print os.path.basename('http://imgbbs.ph.126.net/_FyQQtL0d8zfWS12JiknvA==/2204512017697878635.jpg')
	main()
	# pass