from bs4 import BeautifulSoup
from urllib2 import urlopen,HTTPError
from ghost import Ghost
import os

baseUrl="www.dm5.com"
ghost = Ghost()

class PageList:
	def __init__(self):
		self.pages=[]
	
	def addOnePage(self,onePage):
		self.pages.append(onePage)


def connectHttpFromDomain(requestUrl):
	print 'request '+requestUrl
	try:
		conn = urlopen("http://"+requestUrl)
		data = conn.read()
		conn.close()
		return data
	except HTTPError:
		print 'HTTPError on',requestUrl
		return None

def downloadFilebyUrl(requestUrl,FileName,direc):
	print 'downloading '+requestUrl
	try:
		conn = urlopen(requestUrl)
		target = open(direc+FileName, "wb")
		target.write(conn.read())
		conn.close()
		target.close()
	except HTTPError:
		print 'HTTPError on',requestUrl


if __name__ == '__main__':
	# baseCount=3332
	# fileCount=23
	# with ghost.start() as session:
		# page, _ = session.open("http://"+baseUrl+'/m'+str(baseCount)+'/')
		# if page.http_status==200:
			# result = BeautifulSoup(session.content,'html.parser')
			# selectList = result.find("select",attrs={"id": "pagelist"})
			# pagelist=[ele["value"] for ele in selectList.select("option")]
			# with open("dmpic//"+str(fileCount)+".txt","wb") as tempFile:
				# for onep in pagelist:
					# tempFile.write(onep+"\n")
	with open("dmpic//1.txt","r") as tempRead:
		with open("dmpic//1url.txt","wb") as tempWrite:
			for line in tempRead:
				print line
				with ghost.start() as session:
					line=line.replace("\n","")
					page, _ = session.open("http://"+baseUrl+line)
					if page.http_status==200:
						presult = BeautifulSoup(session.content,'html.parser')
						cpImage=presult.find("img",attrs={"id":"cp_image"})
						tempWrite.write(cpImage["src"])