import scrapy,os


class BeautylegVideoSpider(scrapy.Spider):
	name = "beautylegvideo"

	def __init__(self, murl=None, mname=None, mcookie=None, *args, **kwargs):
		super(BeautylegVideoSpider, self).__init__(*args, **kwargs)
		self.topDir="D:/troopar"
		self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6','Authorization':'Basic bWFjY2hpY2tlbjpGdFVsNHJlYQ==','Cache-Control':'max-age=0','Connection':'keep-alive','Content-Type':'application/x-www-form-urlencoded','Host':'www.beautyleg.com','Origin':'http://www.beautyleg.com','Referer':'http://www.beautyleg.com/member/index.php','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
		self.modelUrl=murl
		self.modelName=mname
		self.myCookie=mcookie
		self.videoLinks=[]

	def start_requests(self):
		yield scrapy.Request(url="http://www.beautyleg.com{}".format(self.modelUrl), headers=self.myheaders, cookies={"PHPSESSID":self.myCookie},callback=self.parse)

	def parse(self, response):
		for aLink in response.css('a'):
			videoLink=aLink.xpath('@href').extract()[0]
			if "video_no" in videoLink:
				yield scrapy.Request(url="http://www.beautyleg.com/member/{}".format(videoLink), headers=self.myheaders, cookies={"PHPSESSID":self.myCookie},callback=self.saveActualLink)

	def saveActualLink(self,response):
		actualLink=response.css("a").xpath('@href').extract()[0]
		self.videoLinks.append(actualLink)

	def spider_closed(self):
		with open("{}/beautylegVideo/{}.txt".format(self.topDir,self.modelName),"ab") as tempWrite:
			for oneLink in self.videoLinks:
				tempWrite.write("{} {}\n".format(oneLink,self.modelName))