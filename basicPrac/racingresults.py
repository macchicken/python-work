from httplib import HTTPConnection
from bs4 import BeautifulSoup
import re,xlsxwriter


baseUrl="www.racingresults.com.au"

class Match:
	def __init__(self,state,location,time):
		self.state=state
		self.location=location
		self.time=time
		self.racingMatches=[]
	
	def getState(self):
		return self.state
	def getLocation(self):
		return self.location
	def getTime(self):
		return self.time
	def getRacingMatches(self):
		return self.racingMatches
	def addRacingMatch(self,oneMatch):
		self.racingMatches.append(oneMatch)

class MatchData:
	def __init__(self,position,onumber,horseBarrier,jockey,trainer,matchName,match):
		self.position=position
		self.onumber=onumber
		self.horseBarrier=horseBarrier
		self.jockey=jockey
		self.trainer=trainer
		self.matchName=matchName
		self.match=match
	
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
	def getMatch(self):
		return self.match


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
	result=BeautifulSoup(odata,'html.parser')
	accmetings=result.find("div",attrs={"id": "accordion-meetings"})
	contents=[cont for cont in accmetings.contents if cont!=u'\n']
	i=0
	wholeMatches=[]
	while i<len(contents):
		con=contents[i]
		state=con.select("span.state")[0].string
		location=con.select("span.location")[0].string
		time=con.select("span.date")[0].string
		onePlace=Match(state,location,time)
		placeMatches=contents[i+1].select("a")
		for pma in placeMatches:
			onePlace.addRacingMatch(pma["href"])
		wholeMatches.append(onePlace)
		i=i+2
	with open(onemFile+".txt","wb") as temp:
		for wm in wholeMatches:
			for rurl in wm.getRacingMatches():
				temp.write(rurl+"\n")
	matchexcelResult=[]
	for wm in wholeMatches:
		state=wm.getState()
		location=wm.getLocation()
		time=wm.getTime()
		racingMatches=wm.getRacingMatches()
		for oneMatch in racingMatches:
			print "%s,%s" % (onemdate,oneMatch)
			onePlaceMatchName=oneMatch.split('/')[-2:-1][0]
			opdata,opstatus,_,_,_=connectHttpFromDomain(baseUrl,oneMatch)
			opsoup=BeautifulSoup(opdata,'html.parser')
			players=opsoup.find_all("a", attrs={"class": "accordion-anchor"})
			for onep in players:
				position=onep.select("span.position")[0].string
				if position is None: position=onep.select("abbr")[0].string
				else: position=position.replace("\n",'')
				onumber=onep.select("span.number")[0].string
				horseBarrier=onep.select("span.horse-barrier")[0].string
				jockey=onep.select("span.jockey")[0].string
				trainer=onep.select("span.trainer")[0].string
				matchexcelResult.append(MatchData(position=position,onumber=onumber,horseBarrier=horseBarrier,jockey=jockey,trainer=trainer,matchName=onePlaceMatchName,match=Match(state,location,time)))
	workbook = xlsxwriter.Workbook("result/"+onemFile+'-result.xlsx')
	worksheet = workbook.add_worksheet()
	worksheet.write(0,0,"State")
	worksheet.write(0,1,"Location")
	worksheet.write(0,2,"Time")
	worksheet.write(0,3,"Match")
	worksheet.write(0,4,"Finish")
	worksheet.write(0,5,"N0")
	worksheet.write(0,6,"Horse(Barrier)")
	worksheet.write(0,7,"Jockey")
	worksheet.write(0,8,"Trainer")
	row=1
	for one in matchexcelResult:
		place=one.getMatch()
		worksheet.write(row,0,place.getState())
		worksheet.write(row,1,place.getLocation())
		worksheet.write(row,2,place.getTime())
		worksheet.write(row,3,one.getMatchName())
		worksheet.write(row,4,one.getPosition())
		worksheet.write(row,5,one.getOnumber())
		worksheet.write(row,6,one.getHorseBarrier())
		worksheet.write(row,7,one.getJockey())
		worksheet.write(row,8,one.getTrainer())
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
