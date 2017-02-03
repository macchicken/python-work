import scrapy,os,datetime
from bs4 import BeautifulSoup


class EventbriteMaxpageSpider(scrapy.Spider):
	name = "eventbritemaxpage"

	def __init__(self, gday=None, gmonth=None, *args, **kwargs):
		super(EventbriteMaxpageSpider, self).__init__(*args, **kwargs)
		self.topDir="D:/troopar"
		self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch, br', 'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6', 'Connection':'keep-alive', 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36', 'Upgrade-Insecure-Requests':'1', 'Host':'www.eventbrite.com.au'}
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
			self.siteDomain="https://www.eventbrite.com.au/d/singapore--singapore/events/"
			self.max=0
		except:
			print "init error"

	def start_requests(self):
		timeStr='{}/{}/{}'.format(self.day,self.month,self.year)
		yield self.makeRequest(1,timeStr)

	def parse(self, response):
		pageData=BeautifulSoup(response.body,'html.parser')
		pagination=pageData.find("ul",attrs={"class":"pagination__navigation-group"})
		navpages=pagination.find_all("a")
		for navpage in navpages:
			if self.max<int(navpage["data-page"]): self.max=int(navpage["data-page"])

	def spider_closed(self):
		with open("{}/maxpage.txt".format(self.topDir),"wb") as tempWrite:
			tempWrite.write(str(self.max))

	def makeRequest(self,counter,timeStr):
		return scrapy.Request(url='{}?crt=regular&end_date={}&page={}&sort=best&start_date={}'.format(self.siteDomain,timeStr,counter,timeStr), headers=self.myheaders, cookies={"mgrefby":"","G":"v%3D2%26i%3Dfe0fee4e-036f-43c3-8e92-016105e5d4dd%26a%3D713%26s%3Dfbbd64ff6e392914ac5893eed63618cb313d338c","eblang":"lo%3Den_AU%26la%3Den-au","mgref":"typeins","_msuuid_8095t6t28384":"616753BE-754C-462F-A215-11E7E0B24024","csrftoken":"e7c3716bb5894ccc8ddfe3ba0516b040","SERVERID":"djc13","_ga":"GA1.3.1736813881.1460709150","ebGAClientId":"1736813881.1460709150","__ar_v4":"NCAKWKGINZDOHPIE6ODGXG%3A20160921%3A8%7COLYYNVG2WJETJN24OFPJMG%3A20160921%3A8%7CHB24VVXCLVCZ5JYSJKZ6OC%3A20160921%3A8","SS":"AE3DLHT-xCoIjxh7PYzLPbRrnzU1nQo3hg","SP":"AGQgbbkLEdrohb6X-Rue4Hh1NOjGVpx7AS2ItClyedfI0AP0TXrUJw49ncHlkI6eRSFX22bYbmY8iSAm-gB5SuakKbrKXHooWmecc32mR6l17iOlywja2BfaSEXNzkK8oSDGXQWCLdxwt2DXE5Qdzaf2ywYCX3QwOyZV67TrwkQmcHX0DnqhpYp0v4PRoi0cx0bbX-yZROq8VgWw4RWLSa3COMXNlASK7FhSLo5lErL_umTKIgJajhM"},dont_filter=True,callback=self.parse)