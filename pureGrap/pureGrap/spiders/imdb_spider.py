import scrapy,os
from bs4 import BeautifulSoup


class IMDBSpider(scrapy.Spider):
	name = "imdbspider"

	def __init__(self, myear=None, *args, **kwargs):
		super(IMDBSpider, self).__init__(*args, **kwargs)
		self.syear=myear
		self.topDir="D:/troopar/imdb/movie"
		self.workingdir="{}/{}".format(self.topDir,myear)
		self.myheaders={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Accept-Encoding":"gzip, deflate, sdch","Accept-Language":"zh-CN,zh;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36","Referer":"http://www.imdb.com/search/title?release_date=2016&view=advanced","Host":"www.imdb.com","Cache-Control":"max-age=0","Connection":"keep-alive"}
		self.mycookie={}
		if not os.path.isdir(self.topDir): os.mkdir(self.topDir)
		if not os.path.isdir(self.workingdir): os.mkdir(self.workingdir)
		with open("{}/imdbcookie.txt".format(self.topDir)) as tempRead:
			for line in tempRead:
				newLine=line.split(":",1)
				self.mycookie[newLine[0]]=newLine[1]

	def start_requests(self):
		for i in range (200,250):
			pageUrl="http://www.imdb.com/search/title?release_date={}&view=advanced&page={}&ref_=adv_prv".format(self.syear,str(i))
			yield scrapy.Request(url=pageUrl, headers=self.myheaders, cookies=self.mycookie,callback=self.parse)

	def parse(self, response):
		pageResult=BeautifulSoup(response.body,'html.parser')
		items=pageResult.find_all("div",attrs={"class":"lister-item mode-advanced"})
		for item in items:
			itemHeader=item.find("div",attrs={"class":"lister-item-content"}).find("h3",attrs={"class":"lister-item-header"})
			movieUrl="http://www.imdb.com{}".format(itemHeader.select('a')[0]["href"])
			indexno=int(itemHeader.select("span:nth-of-type(1)")[0].contents[0].replace(",","").strip("."))
			yield scrapy.Request(url=movieUrl, headers=self.myheaders, meta={"indexno":indexno},cookies=self.mycookie,callback=self.parseSingle)
			
	def parseSingle(self,response):
		indexno=response.meta['indexno']
		pageNo=indexno/500
		if indexno%500>0:
			pageNo=pageNo+1
		pageResult=BeautifulSoup(response.body,'html.parser')
		title=pageResult.find("meta",attrs={"name":"title"})
		description=pageResult.find("meta",attrs={"name":"description"})
		pageId=pageResult.find("meta",attrs={"property":"pageId"})
		type=pageResult.find("meta",attrs={"property":"og:type"})
		image=pageResult.find("meta",attrs={"property":"og:image"})
		url=pageResult.find("meta",attrs={"property":"og:url"})
		article=pageResult.find("div",attrs={"class":"article","id":"titleDetails"})
		seemore=article.find_all("span",attrs={"class":"see-more inline"})
		boxofficeurl=None
		for one in seemore:
			aele=one.select('a')
			if len(aele)>0 and "business" in aele[0]["href"]:
				boxofficeurl=one.select('a')[0]["href"]
				break
		contens=[]
		contens.append({"tagName":"pageId","content":pageId["content"]})
		contens.append({"tagName":"title","content":title["content"].encode("utf-8")})
		contens.append({"tagName":"description","content":description["content"].encode("utf-8")})
		contens.append({"tagName":"type","content":type["content"]})
		contens.append({"tagName":"image","content":image["content"]})
		contens.append({"tagName":"url","content":url["content"]})
		if boxofficeurl is not None:
			boxofficeurl="{}{}".format(url["content"],boxofficeurl)
			yield scrapy.Request(url=boxofficeurl, headers=self.myheaders, meta={"pageNo":str(pageNo),"pageId":pageId["content"],"contens":contens},cookies=self.mycookie,callback=self.getboxoffice)
		else:
			self.saveDataToFile("{}/{}/{}.txt".format(self.workingdir,str(pageNo),pageId["content"]),contens)

	def getboxoffice(self,response):
		pageNo=response.meta['pageNo']
		pageId=response.meta['pageId']
		contens=response.meta['contens']
		pageResult=BeautifulSoup(response.body,'html.parser')
		tn15content=pageResult.find("div",attrs={"id":"tn15content"}).contents
		tagName=None
		oneline=""
		for content in tn15content:
			contentstr=content.encode("utf-8").replace("\n","")
			if contentstr.startswith("<hr"): break
			if contentstr.startswith("<h5>"):
				tagName=contentstr.replace("<h5>","").replace("</h5>","")
			elif not contentstr.startswith("<br"):
				oneline=oneline+contentstr
			else:
				oneline=oneline.strip()
				if len(oneline)>0:
					contens.append({"tagName":tagName,"content":oneline})
				oneline=""
		self.saveDataToFile("{}/{}/{}.txt".format(self.workingdir,pageNo,pageId),contens)
	
	def saveDataToFile(self,fileName,contens):
		with open(fileName,"wb") as tempWrite:
			for content in contens:
				tempWrite.write("{}\n{}\n-----------\n".format(content["tagName"],content["content"]))

	def spider_closed(self):
		pass
