from bs4 import BeautifulSoup
import datetime,urllib2,gzip,traceback,sys,os
from StringIO import StringIO

siteDomain="http://www.roadtovr.com"

class BlogData:
	def __init__(self,bTitle,bSubTitle,bAuthor,bPostDate,burl):
		self.bTitle=bTitle
		self.bSubTitle=bSubTitle
		self.bAuthor=bAuthor
		self.bPostDate=bPostDate
		self.burl=burl
	
	def getBtitle(self):
		return self.bTitle
	
	def getBurl(self):
		return self.burl


def getContentFromTag(htmlTag,key=None):
	if (len(htmlTag)==0):return " "
	else:
		if key is None: return htmlTag[0].string
		else: return htmlTag[0][key]

def connectHttpFromDomain(domainName,requestUrl):
	request = urllib2.Request(domainName+requestUrl)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)
	try:
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO(response.read())
			with gzip.GzipFile(fileobj=buf) as f:
				return f.read()
		else: return response.read()
	except:
		traceback.print_exc(file=sys.stdout)
	finally:
		response.close()


if __name__ == '__main__':
	dirPath="roadtovr/roadtovr_"+str(datetime.date.today())
	if not os.path.isdir(dirPath):
		os.mkdir(dirPath)
	data = connectHttpFromDomain(siteDomain,"/")
	if data is not None:
		result=BeautifulSoup(data,'html.parser')
		matchesItem=result.find_all("div",attrs={"class": "item-details"})
		blogUrl=[]
		for oneItem in matchesItem:
			burl=getContentFromTag(oneItem.select("[itemprop=url]"),"href")
			blogUrl.append(burl)
		for one in blogUrl:
			fileName=one.split('/')[-2:-1][0]
			odata = connectHttpFromDomain(one,"")
			oresult=BeautifulSoup(odata,'html.parser')
			postHeader=oresult.select(".td-post-header")
			postContent=oresult.select(".td-post-content")
			postFooter=oresult.select("footer")
			if len(postHeader)==1:
				blogTitle=getContentFromTag(postHeader[0].select(".entry-title"))
				blogSubTitle=getContentFromTag(postHeader[0].select(".td-post-sub-title"))
				blogAuthor=getContentFromTag(postHeader[0].select("[itemprop=author]"))
				blogCreatedDate=getContentFromTag(postHeader[0].select("[itemprop=dateCreated]"),"datetime")
				print "%s,%s,%s,%s" %(blogTitle,blogSubTitle,blogAuthor,blogCreatedDate)
				if len(postContent)==1:
					with open(dirPath+'/'+fileName,"wb") as posContent:
						posContent.write(("%s,%s,%s,%s\n" %(blogTitle,blogSubTitle,blogAuthor,blogCreatedDate)).encode('utf8'))
						ps=postContent[0].select("p,audio,figure")
						for p in ps:
							posContent.write(str(p))
						posContent.write("\n")
						if len(postFooter)==1:
							posContent.write(str(postFooter[0]))