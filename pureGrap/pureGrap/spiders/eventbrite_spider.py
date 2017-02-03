import scrapy,os,datetime,pureGrap.myLogger,copy,json,xlsxwriter,shutil,re
from bs4 import BeautifulSoup


class EventbriteSpider(scrapy.Spider):
	name = "eventbrite"

	def __init__(self, gday=None, gmonth=None, *args, **kwargs):
		super(EventbriteSpider, self).__init__(*args, **kwargs)
		self.topDir="D:/troopar"
		self.eliminatingStr="[^a-zA-Z0-9\-\@]"
		self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6', 'Connection':'keep-alive', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36', 'Upgrade-Insecure-Requests':'1', 'Host':'www.eventbrite.com.au'}
		self.myCookie={"mgrefby":"","G":"v%3D2%26i%3Dfe0fee4e-036f-43c3-8e92-016105e5d4dd%26a%3D713%26s%3Dfbbd64ff6e392914ac5893eed63618cb313d338c","eblang":"lo%3Den_AU%26la%3Den-au","mgref":"typeins","_msuuid_8095t6t28384":"616753BE-754C-462F-A215-11E7E0B24024","csrftoken":"e7c3716bb5894ccc8ddfe3ba0516b040","SERVERID":"djc13","_ga":"GA1.3.1736813881.1460709150","ebGAClientId":"1736813881.1460709150","__ar_v4":"NCAKWKGINZDOHPIE6ODGXG%3A20160921%3A8%7COLYYNVG2WJETJN24OFPJMG%3A20160921%3A8%7CHB24VVXCLVCZ5JYSJKZ6OC%3A20160921%3A8","SS":"AE3DLHT-xCoIjxh7PYzLPbRrnzU1nQo3hg","SP":"AGQgbbkLEdrohb6X-Rue4Hh1NOjGVpx7AS2ItClyedfI0AP0TXrUJw49ncHlkI6eRSFX22bYbmY8iSAm-gB5SuakKbrKXHooWmecc32mR6l17iOlywja2BfaSEXNzkK8oSDGXQWCLdxwt2DXE5Qdzaf2ywYCX3QwOyZV67TrwkQmcHX0DnqhpYp0v4PRoi0cx0bbX-yZROq8VgWw4RWLSa3COMXNlASK7FhSLo5lErL_umTKIgJajhM"}
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
			self.siteDomain="https://www.eventbrite.com.au/d/singapore--singapore/events/"
			self.country="Singapore"
			self.asyncLogger=pureGrap.myLogger.AsyncLogging("webscrapingEventbrite",self.errorLog)
			with open("{}/maxpage.txt".format(self.topDir),"rb") as tempRead:
				self.max=int(tempRead.readline())
			self.keyFileName="result-eventbrite-singapore"
			fileName="{}/{}-{}{}.xlsx".format(self.dirPath,self.keyFileName,self.month,self.day)
			if os.path.isfile(fileName):
				lastCheckTime="%s_%s_%s_%s_%s_%s" % (now.year,now.month,now.day,now.hour,now.minute,now.second)
				shutil.copyfile(fileName,"{}/{}-{}{}-{}.xlsx".format(self.dirPath,self.keyFileName,self.month,self.day,lastCheckTime))
			self.eventResults=[]
		except:
			print "init error"

	def start_requests(self):
		timeStr='{}/{}/{}'.format(self.day,self.month,self.year)
		maxCounter=self.max+1
		for i in range(maxCounter):
			yield scrapy.Request(url='{}?crt=regular&end_date={}&page={}&sort=best&start_date={}'.format(self.siteDomain,timeStr,i,timeStr), headers=self.myheaders, cookies=self.myCookie,dont_filter=True,callback=self.parse)

	def parse(self, response):
		pageData=BeautifulSoup(response.body,'html.parser')
		tempList=pageData.find_all("div",attrs={"class": "js-d-poster"})
		for onee in tempList:
			eventUrl=onee.find("a",attrs={"class":"js-event-link"})["href"]
			headers=copy.deepcopy(self.myheaders)
			headers["Accept-Encoding"]="gzip, deflate, sdch"
			headers["Host"]=eventUrl.split("/")[2]
			yield scrapy.Request(url=eventUrl,headers=headers, cookies=self.myCookie, dont_filter=True,callback=self.parseOneEvent)

	def parseOneEvent(self,response):
		try:
			pageData=BeautifulSoup(response.body,'html.parser')
			title=pageData.select("[property=og:title]")[0]["content"]
			image=pageData.select("[property=og:image]")[0]["content"]
			evurl=pageData.select("[property=og:url]")[0]["content"]
			description=pageData.select("[property=og:description]")[0]["content"]
			startDate=pageData.select("[property=event:start_time]")[0]["content"]
			endDate=pageData.select("[property=event:end_time]")[0]["content"]
			latitude=pageData.select("[property=event:location:latitude]")[0]["content"]
			longitude=pageData.select("[property=event:location:longitude]")[0]["content"]
			ldJson=json.loads(pageData.find("script",attrs={"type":"application/ld+json"}).contents[0].strip())
			if "offers" in ldJson:
				offers=ldJson["offers"]
				if "lowPrice" in offers:
					requires=str(offers["lowPrice"])
				elif "highPrice" in offers:
					requires=str(offers["highPrice"])
				else:
					requires="0"
			else:
				requires="0"
			yield scrapy.Request(url="{}?latlng={},{}".format("http://maps.googleapis.com/maps/api/geocode/json",latitude,longitude),meta={'eventObj':{"title":title,"image":image,"description":description,"startDate":startDate,"endDate":endDate,"latitude":latitude,"longitude":longitude,"evurl":evurl,"requires":requires,"address":""}},dont_filter=True,callback=self.addAddress)
		except:
			self.asyncLogger.logToFile("debug")

	def addAddress(self,response):
		eventObj=response.meta['eventObj']
		jdata=json.loads(response.body)
		if jdata["status"]=="OK":
			addressResults=jdata["results"]
			if len(addressResults)>0:
				address=addressResults[0]["formatted_address"]
			else: address=""
		else: address=""
		eventObj["address"]=address
		self.eventResults.append(eventObj)

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
				worksheet.write(row,4,oneEv["evurl"])
				worksheet.write(row,5,oneEv["image"])
				worksheet.write(row,6,oneEv["address"])
				worksheet.write(row,9,oneEv["evurl"])
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