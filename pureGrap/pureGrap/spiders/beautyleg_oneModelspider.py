import scrapy,os


class BeautylegOneModelSpider(scrapy.Spider):
	name = "beautylegoneModel"

	def __init__(self, mname=None, mcookie=None, *args, **kwargs):
		super(BeautylegOneModelSpider, self).__init__(*args, **kwargs)
		self.topDir="D:/troopar"
		self.myheaders = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-GB,en-US;q=0.8,en;q=0.6',
		'Authorization':'Basic bWFjY2hpY2tlbjpGdFVsNHJlYQ==',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Host':'www.beautyleg.com',
		'Origin':'http://www.beautyleg.com',
		'Referer':'http://www.beautyleg.com/member/index.php',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
		self.myCookie=mcookie
		self.modelName=mname
		self.modelDir="{}/beautyleg/{}".format(self.topDir,mname)
		self.modelFile="{}/beautyleg/{}.txt".format(self.topDir,mname)
		if not os.path.isdir(self.modelDir): os.mkdir(self.modelDir)

	def start_requests(self):
		with open(self.modelFile,"rb") as tempRead:
			for line in tempRead:
				albumUrl=line.strip("\n")
				yield scrapy.Request(url="http://www.beautyleg.com{}".format(albumUrl),headers=self.myheaders,meta={'albumUrl':albumUrl},cookies={"PHPSESSID":self.myCookie},callback=self.parse)

	def parse(self, response):
		albumNo=response.meta['albumUrl'].split("no=")[1]
		albumDir="{}/{}".format(self.modelDir,albumNo)
		if not os.path.isdir(albumDir): os.mkdir(albumDir)
		for aLink in response.css('a'):
			fileUrl=aLink.xpath('@href').extract()[0]
			fileName=fileUrl.split('/')[-1:][0]
			yield scrapy.Request(url="http://www.beautyleg.com{}".format(fileUrl),headers=self.myheaders,cookies={"PHPSESSID":self.myCookie},meta={'fileName': "{}/{}".format(albumDir,fileName)},callback=self.saveFileToDisk)

	def saveFileToDisk(self,response):
		with open(response.meta['fileName'], "wb") as target:
			target.write(response.body)

	def spider_closed(self):
		pass