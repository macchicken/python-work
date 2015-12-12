from httplib import HTTPConnection
from bs4 import BeautifulSoup
import re,xlsxwriter


baseUrl="www.racingresults.com.au"

class MatchData:
	def __init__(self,position,onumber,horseBarrier,jockey,trainer,matchName):
		self.position=position
		self.onumber=onumber
		self.horseBarrier=horseBarrier
		self.jockey=jockey
		self.trainer=trainer
		self.matchName=matchName
	
	def getPosition(self):
		return self.position
	def getOnumber(self):
		return self.onumber
	def getHorseBarrier(self):
		return self.horseBarrier
	def getJockey(self):
		return self.jockey
	def getTrainer(self):
		return self.trainer
	def getMatchName(self):
		return self.matchName


def findtags(text):
	if text is not None and text.strip()!='':
		return re.findall(r'<\s*[a-zA-Z0-9]+\s*(?:\w+\s*=\s*"[^"]*"\s*)*\s*>',text)
	else: return []

def connectHttpFromDomain(domainName,requestUrl):
	conn = HTTPConnection(domainName)
	conn.request("GET", requestUrl)
	r1 = conn.getresponse()
	content_type=r1.getheader('content-type')
	content_disposition=r1.getheader('content-disposition')
	reason=r1.reason
	status=r1.status
	data = r1.read() #whole response data
	conn.close()
	return data,status,reason,content_type,content_disposition

def getOneMatchData(onemFile,onemdate):
	odata,ostatus,_,_,_=connectHttpFromDomain(baseUrl,onemdate)
	result=findtags(odata)
	resultURL=[]
	for r in result:
		if 'race' in r and '<a href=' in r and 'linkExternal' not in r:
			tmpr=BeautifulSoup(r,'html.parser')
			resultURL.append(tmpr.find('a')["href"])
	with open(onemFile+".txt","wb") as temp:
		for rurl in resultURL: temp.write(rurl+"\n")
	matchResult=[]
	matchexcelResult=[]
	for onePlaceMatch in resultURL:
		print "%s,%s" % (onemdate,onePlaceMatch)
		onePlaceMatchName=onePlaceMatch.split('/')[-2:-1][0]
		opdata,opstatus,_,_,_=connectHttpFromDomain(baseUrl,onePlaceMatch)
		opsoup=BeautifulSoup(opdata,'html.parser')
		players=opsoup.find_all("a", attrs={"class": "accordion-anchor"})
		playersStr=""
		for onep in players:
			position=onep.select("span.position")[0].string
			if position is None: position=onep.select("abbr")[0].string
			else: position=position.replace("\n",'')
			onumber=onep.select("span.number")[0].string
			horseBarrier=onep.select("span.horse-barrier")[0].string
			jockey=onep.select("span.jockey")[0].string
			trainer=onep.select("span.trainer")[0].string
			playersStr=playersStr+"Finish:%s N0:%s Horse(Barrier):%s Jockey:%s Trainer:%s\n" % (position,onumber,horseBarrier,jockey,trainer)
			matchexcelResult.append(MatchData(position=position,onumber=onumber,horseBarrier=horseBarrier,jockey=jockey,trainer=trainer,matchName=onePlaceMatchName))
		matchResult.append(onePlaceMatchName+"\n"+playersStr)
	with open("result/"+onemFile+"-result.txt","wb") as temp:
		for mr in matchResult: temp.write(mr)
	workbook = xlsxwriter.Workbook("result/"+onemFile+'-result.xlsx')
	worksheet = workbook.add_worksheet()
	worksheet.write(0,0,"Match")
	worksheet.write(0,1,"Finish")
	worksheet.write(0,2,"N0")
	worksheet.write(0,3,"Horse(Barrier)")
	worksheet.write(0,4,"Jockey")
	worksheet.write(0,5,"Trainer")
	row=1
	for one in matchexcelResult:
		worksheet.write(row,0,one.getMatchName())
		worksheet.write(row,1,one.getPosition())
		worksheet.write(row,2,one.getOnumber())
		worksheet.write(row,3,one.getHorseBarrier())
		worksheet.write(row,4,one.getJockey())
		worksheet.write(row,5,one.getTrainer())
		row=row+1


if __name__ == '__main__':
	# data,status,reason,content_type,content_disposition=connectHttpFromDomain(baseUrl,'')
	# soup=BeautifulSoup(data,'html.parser')
	# tabresult=soup.find_all('table')
	# for tab in tabresult:
		# if tab["class"]==[u'bigcal']:
			# racing=tab.find_all('td')
			# raingmatches=[]
			# for ra in racing:
				# spans=ra.select("a > span.notice > span")
				# if int(spans[0].string)>0:
					# raingmatches.append(ra.select("a")[0]["href"])
			# break
	# for onemdate in raingmatches:
		# onemFile=onemdate.split("/")[2]
	onemFile=raw_input("enter the date(yyyy-mm-dd) of matches looking for")
	result=re.match(r'[1-9][0-9]{3}-[0-9]{1,2}-[0-9]{1,2}',onemFile)
	if result:
		onemdate="/meetings/"+onemFile+"/"
		print onemdate
		getOneMatchData(onemFile,onemdate)
