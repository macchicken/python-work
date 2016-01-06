from httplib import HTTPConnection
from bs4 import BeautifulSoup
import xlsxwriter,datetime,calendar


siteDomain="www.sydney.com"
baseUrl="/events/search?start_rank="
month="01"
lastDay=str(calendar.monthrange(2016, int(month))[1])
searchCon="&query=&date_from=01-"+month+"-2016&date_to="+lastDay+"-"+month+"-2016"

class EventData:
	def __init__(self,evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg):
		self.evName=evName
		self.evDescription=evDescription
		self.evProductUrl=evProductUrl
		self.evStartDate=evStartDate
		self.evEndDate=evEndDate
		self.evImg=evImg
	
	def getEvName(self):
		return self.evName
	
	def getEvDescription(self):
		return self.evDescription
		
	def getEvProductUrl(self):
		return self.evProductUrl
		
	def getEvStartDate(self):
		return self.evStartDate
	
	def getEvEndDate(self):
		return self.evEndDate
	
	def getEvImg(self):
		return self.evImg

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


if __name__ == '__main__':
	counter=1
	odata,ostatus,_,_,_=connectHttpFromDomain(siteDomain,baseUrl+str(counter)+searchCon)
	oresult=BeautifulSoup(odata,'html.parser')
	matchesItem=oresult.find("p",attrs={"class": "matches"})
	eventResults=[]
	if matchesItem is not None:
		matchesItem=int(matchesItem.string.split()[0])
		if matchesItem>0:
			matchesItemCount=matchesItem/8
			if matchesItem%8>0: matchesItemCount+=1
			events=oresult.find_all("li",attrs={"itemprop": "event"})
			for onee in events:
				eventData=onee.select(".event-data")[0]
				evImg=onee.select("[itemprop=image]")
				if eventData is not None:
					evName=eventData.select("[itemprop=name]")[0].select("a")[0].string
					evDescription=eventData.select("[itemprop=description]")[0].string
					pulr=eventData.select(".product-url")
					if len(pulr)>0:evProductUrl=pulr[0].select("a")[0]["href"]
					else: evProductUrl=""
					evImg=onee.select("[itemprop=image]")
					if len(evImg)>0: evImg=evImg[0]["src"]
					else: evImg=""
					evStartDate=eventData.select("[itemprop=startDate]")[0]["content"]
					evEndDate=eventData.select("[itemprop=endDate]")[0]["content"]
					eventResults.append(EventData(evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg))
			counter+=1
			while counter<=matchesItemCount:
				print counter
				odata,ostatus,_,_,_=connectHttpFromDomain(siteDomain,baseUrl+str(1+(counter-1)*8)+searchCon)
				oresult=BeautifulSoup(odata,'html.parser')
				events=oresult.find_all("li",attrs={"itemprop": "event"})
				for onee in events:
					eventData=onee.select(".event-data")[0]
					if eventData is not None:
						evName=eventData.select("[itemprop=name]")[0].select("a")[0].string
						evDescription=eventData.select("[itemprop=description]")[0].string
						pulr=eventData.select(".product-url")
						if len(pulr)>0:evProductUrl=pulr[0].select("a")[0]["href"]
						else: evProductUrl=""
						evImg=onee.select("[itemprop=image]")
						if len(evImg)>0: evImg=evImg[0]["src"]
						else: evImg=""
						evStartDate=eventData.select("[itemprop=startDate]")[0]["content"]
						evEndDate=eventData.select("[itemprop=endDate]")[0]["content"]
						eventResults.append(EventData(evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg))
				counter+=1
	workbook = xlsxwriter.Workbook("event/result-cityofsydney-"+month+".xlsx")
	worksheet = workbook.add_worksheet()
	worksheet.write(0,0,"StartDate")
	worksheet.write(0,1,"EndDate")
	worksheet.write(0,2,"Name")
	worksheet.write(0,3,"Description")
	worksheet.write(0,4,"ProductUrl")
	worksheet.write(0,5,"Image")
	row=1
	for oneEv in eventResults:
		worksheet.write(row,0,oneEv.getEvStartDate())
		worksheet.write(row,1,oneEv.getEvEndDate())
		worksheet.write(row,2,oneEv.getEvName())
		worksheet.write(row,3,oneEv.getEvDescription())
		worksheet.write(row,4,oneEv.getEvProductUrl())
		worksheet.write(row,5,oneEv.getEvImg())
		row+=1
	workbook.close()