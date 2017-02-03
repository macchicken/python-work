import scrapy,os,datetime,pureGrap.myLogger,copy,json,xlsxwriter,shutil,re
from bs4 import BeautifulSoup


class WhatshappeningsgSpider(scrapy.Spider):
	name = "whatshappeningsg"

	def __init__(self, gday=None, gmonth=None, *args, **kwargs):
		super(WhatshappeningsgSpider, self).__init__(*args, **kwargs)
		self.topDir="D:/troopar"
		self.eliminatingStr="[^a-zA-Z0-9\-\@]"
		self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6','Connection':'keep-alive','Host':'www.whatshappening.sg','Referer':'http://www.whatshappening.sg/events/index.php?d=2016-09-22&m=1','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36','Upgrade-Insecure-Requests':'1'}
		self.myCookie={"helios_9f9cd63c14a22c52f62e358535f47b8f":"hgla5v6v0t3jo2kdk7bge6ci57","__utmt":"1","__utma":"217362000.774928566.1474351692.1474421244.1474423088.3","__utmb":"217362000.2.10.1474423088","__utmc":"217362000","__utmz":"217362000.1474351695.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)","__unam":"2f1607e-15746358f6a-69697270-13"}
		try:
			now=datetime.datetime.now()
			if not os.path.isdir(self.topDir+"/event"): os.mkdir(self.topDir+"/event")
			self.year=str(now.year)
			if now.month<10: self.month="0"+str(now.month)
			else: self.month=str(now.month)
			if gmonth is not None:
				self.month=gmonth
			if now.day<10: self.day="0"+str(now.day)
			else: self.day=str(now.day)
			if gday is not None:
				self.day=gday
			self.dirPath=self.topDir+"/event/"+self.year
			if not os.path.isdir(self.dirPath): os.mkdir(self.dirPath)
			self.imageDirPath=self.dirPath+"/"+"image"
			if not os.path.isdir(self.imageDirPath): os.mkdir(self.imageDirPath)
			logDir="{}/log".format(self.dirPath)
			if not os.path.isdir(logDir): os.mkdir(logDir)
			date="%s-%s-%s" % (self.year,self.month,str(now.day))
			self.errorLog="%s/%s-%s.log" %(logDir,"error",date)
			self.siteDomain="http://www.whatshappening.sg/events/index.php"
			self.country="Singapore"
			self.asyncLogger=pureGrap.myLogger.AsyncLogging("webscrapingWhatshappeningsg",self.errorLog)
			self.keyFileName="result-whatshappening-singapore"
			fileName="{}/{}-{}{}.xlsx".format(self.dirPath,self.keyFileName,self.month,self.day)
			if os.path.isfile(fileName):
				lastCheckTime="%s_%s_%s_%s_%s_%s" % (now.year,now.month,now.day,now.hour,now.minute,now.second)
				shutil.copyfile(fileName,"{}/{}-{}{}-{}.xlsx".format(self.dirPath,self.keyFileName,self.month,self.day,lastCheckTime))
			self.eventResults=[]
		except:
			print "init error"

	def start_requests(self):
		timeStr='{}-{}-{}'.format(self.year,self.month,self.day)
		yield scrapy.Request(url='{}?d={}&m=1'.format(self.siteDomain,timeStr),headers=self.myheaders,cookies=self.myCookie,dont_filter=True,callback=self.parse)

	def parse(self, response):
		pageData=BeautifulSoup(response.body,'html.parser')
		matchItems=pageData.find("table",attrs={"class": "event-list-table"})
		trCollections=matchItems.find_all("tr")
		for onee in trCollections:
			eventUrl=onee.find("a",attrs={"itemprop":"name"})["href"]
			yield scrapy.Request(url=eventUrl,headers=self.myheaders,cookies=self.myCookie,dont_filter=True,callback=self.parseOneEvent)

	def parseOneEvent(self,response):
		try:
			pageData=BeautifulSoup(response.body,'html.parser')
			httpEquiv=pageData.select("[http-equiv=Content-Type]")[0]["content"]
			if len(httpEquiv)>0:
				charset=httpEquiv.split("charset=")[1]
			else:
				charset='ISO-8859-1'
			title=pageData.select("[property=og:title]")[0]["content"]
			temp=str(pageData.find("meta",attrs={"property":"og:description"}))
			description=temp.split('"')[1].decode(charset)
			tStartDate=pageData.select("[itemprop=startDate]")[0]
			startDate=tStartDate["content"]
			endDate=tStartDate.contents[0]
			tlatitude=pageData.select("[itemprop=latitude]")
			if len(tlatitude)>0:
				latitude=tlatitude[0]["content"]
			else:
				latitude=0
			tlongitude=pageData.select("[itemprop=longitude]")
			if len(tlongitude)>0:
				longitude=tlongitude[0]["content"]
			else:
				longitude=0
			address='{} {}'.format(pageData.select("[itemprop=streetAddress]")[0].contents[0],pageData.select("[itemprop=addressCountry]")[0].contents[0])
			timage=pageData.select("[itemprop=description]")[0].select("img")
			if len(timage)>0:
				image=timage[0]["src"]
			else:
				image=""
			self.eventResults.append({"title":title,"image":image,"description":description,"startDate":startDate,"endDate":endDate,"latitude":latitude,"longitude":longitude,"eventUrl":response.url,"requires":"","address":address})
		except:
			self.asyncLogger.logToFile("debug")

	def spider_closed(self):
		workbook = xlsxwriter.Workbook("{}/{}-{}{}.xlsx".format(self.dirPath,self.keyFileName,self.month,self.day))
		worksheet = workbook.add_worksheet()
		worksheet.write(0,0,"startDate")
		worksheet.write(0,1,"endDate")
		worksheet.write(0,2,"name")
		worksheet.write(0,3,"description")
		worksheet.write(0,4,"productUrl")
		worksheet.write(0,5,"image")
		worksheet.write(0,6,"location")
		worksheet.write(0,7,"longitude")
		worksheet.write(0,8,"latitude")
		worksheet.write(0,9,"url")
		worksheet.write(0,10,"contact")
		worksheet.write(0,11,"userId")
		worksheet.write(0,12,"approveToJoin")
		worksheet.write(0,13,"availability")
		worksheet.write(0,14,"requires")
		worksheet.write(0,15,"maxNum")
		worksheet.write(0,16,"localImage")
		row=1
		for oneEv in self.eventResults:
			try:
				worksheet.write(row,0,oneEv["startDate"])
				worksheet.write(row,1,oneEv["endDate"])
				worksheet.write(row,2,re.sub(self.eliminatingStr,' ',oneEv["title"]))
				worksheet.write(row,3,oneEv["description"])
				worksheet.write(row,4,oneEv["eventUrl"])
				worksheet.write(row,5,oneEv["image"])
				worksheet.write(row,6,oneEv["address"])
				worksheet.write(row,9,oneEv["eventUrl"])
				worksheet.write(row,10,"")
				worksheet.write(row,7,oneEv["longitude"])
				worksheet.write(row,8,oneEv["latitude"])
				worksheet.write(row,11,"69")
				worksheet.write(row,12,"auto")
				worksheet.write(row,13,"public")
				worksheet.write(row,14,oneEv["requires"])
				worksheet.write(row,15,"0")
				worksheet.write(row,16,"")
				row+=1
			except:
				self.asyncLogger.logToFile("debug")
		workbook.close()