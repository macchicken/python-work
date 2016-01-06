from httplib import HTTPConnection
from bs4 import BeautifulSoup
import xlsxwriter,datetime


siteDomain="www.sydneyolympicpark.com.au"
baseUrl="/whats_on/upcoming?collection=events&meta_e_orsand=Events&query=%21showallevents%20%25%20D%3D"
searchCon="&specific_date=yes&sort=metaD&start_rank="

class EventData:
	def __init__(self,searchTime,evDate,evTitle,evDescription):
		self.searchTime=searchTime
		self.evDate=evDate
		self.evTitle=evTitle
		self.evDescription=evDescription
	
	def getEvDate(self):
		return self.evDate
	
	def getEvTitle(self):
		return self.evTitle
		
	def getEvDescription(self):
		return self.evDescription
		
	def getSearchTime(self):
		return self.searchTime

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
	beginDay=datetime.date.today()
	excelResults=[]
	for i in range(365):
		print beginDay
		strday=str(beginDay.day)
		if beginDay.day<10: strday='0'+str(beginDay.day)
		else: strday=str(beginDay.day)
		if beginDay.month<10: strmonth='0'+str(beginDay.month)
		else: strmonth=str(beginDay.month)
		strtime=str(beginDay.year)+strmonth+strday
		odata,ostatus,_,_,_=connectHttpFromDomain(siteDomain,baseUrl+strtime+searchCon+"1")
		oresult=BeautifulSoup(odata,'html.parser')
		articles=oresult.find_all("div",attrs={"class": "article-summary"})
		pagesNav=len(oresult.find_all("a",attrs={"class": "fb-next-result-page fb-page-nav"}))
		if len(articles)!=0:
			for onea in articles:
				dateVenue=onea.select(".event-date-venue")
				title=onea.select("h4")
				descriptin=onea.select("p")
				if len(dateVenue)>0: dateVenue=dateVenue[0].string
				else: dateVenue=""
				if len(title)>0: title=title[0].string
				else: title=""
				if len(descriptin)>0: descriptin=descriptin[0].string
				else: descriptin=""
				excelResults.append(EventData(strtime,dateVenue,title,descriptin))
			count=1
			while count<=pagesNav:
				odata,ostatus,_,_,_=connectHttpFromDomain(siteDomain,baseUrl+"20160107"+searchCon+str(1+count*10))
				oresult=BeautifulSoup(odata,'html.parser')
				articles=oresult.find_all("div",attrs={"class": "article-summary"})
				for onea in articles:
					dateVenue=onea.select(".event-date-venue")
					title=onea.select("h4")
					descriptin=onea.select("p")
					if len(dateVenue)>0: dateVenue=dateVenue[0].string
					else: dateVenue=""
					if len(title)>0: title=title[0].string
					else: title=""
					if len(descriptin)>0: descriptin=descriptin[0].string
					else: descriptin=""
					e=excelResults.append(EventData(strtime,dateVenue,title,descriptin))
				count+=1
		beginDay+=datetime.timedelta(days=1)
	workbook = xlsxwriter.Workbook("result-sydneyolympicpark.xlsx")
	worksheet = workbook.add_worksheet()
	worksheet.write(0,0,"Time")
	worksheet.write(0,1,"Date")
	worksheet.write(0,2,"Title")
	worksheet.write(0,3,"Description")
	row=1
	for oneEv in excelResults:
		worksheet.write(row,0,oneEv.getSearchTime())
		worksheet.write(row,1,oneEv.getEvDate())
		worksheet.write(row,2,oneEv.getEvTitle())
		worksheet.write(row,3,oneEv.getEvDescription())
		row+=1
	workbook.close()