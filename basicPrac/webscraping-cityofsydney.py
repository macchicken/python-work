from httplib import HTTPConnection
from bs4 import BeautifulSoup
import xlsxwriter,datetime,calendar,json,re


siteDomain="www.sydney.com"
baseUrl="/events/search?start_rank="
month="02"
lastDay=str(calendar.monthrange(2016, int(month))[1])
searchCon="&query=&date_from=01-"+month+"-2016&date_to="+lastDay+"-"+month+"-2016"
country="Australia"
eliminatingStr="[^a-zA-Z0-9\n\.\,\(\)\-\/\' '\!\?]"

class EventData:
	def __init__(self,evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg,evPlace,evUrl):
		self.evName=evName
		self.evDescription=evDescription
		self.evProductUrl=evProductUrl
		self.evStartDate=evStartDate
		self.evEndDate=evEndDate
		self.evImg=evImg
		self.evPlace=evPlace
		self.evUrl=evUrl
	
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

	def getEvPlace(self):
	    return self.evPlace

	def getEvUrl(self):
		return self.evUrl

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
					evName=re.sub(eliminatingStr, '', evName)
					# evDescription=eventData.select("[itemprop=description]")[0].string
					evDescription=''
					pulr=eventData.select(".product-url")
					if len(pulr)>0:evProductUrl=pulr[0].select("a")[0]["href"]
					else: evProductUrl=""
					evImg=""
					evUrl=onee.select("[itemprop=url]")[0]["href"]
					oodata,oostatus,_,_,_=connectHttpFromDomain(siteDomain,evUrl)
					ooresult=BeautifulSoup(oodata,'html.parser')
					eventImages=ooresult.find_all("div",attrs={"class": "cntImageHolder"})
					aboutBlock=ooresult.find("section",attrs={"class": "about-block"}).select("p")[0]
					for content in aboutBlock.contents:
						if content.string is not None:
							evDescription=evDescription+re.sub(eliminatingStr,'',content.string)
					if len(eventImages)>0: evImg=eventImages[0]["style"].split("url")[1][1:-2]
					# eventDate=eventData.select(".event-date")
					# if len(eventDate)>0: eventPlace=eventDate[0].string.split(',')[1].strip()
					# else: eventPlace=''
					oeventPlace=ooresult.find("div",attrs={"itemprop": "location"})
					streetAddress=oeventPlace.select("[itemprop=streetAddress]")[0].string
					locality=oeventPlace.select("[itemprop=addressLocality]")[0].string
					region=oeventPlace.select("[itemprop=addressRegion]")[0].string
					postCode=oeventPlace.select("[itemprop=postalCode]")[0].string
					eventPlace=streetAddress+' '+locality+' '+region+' '+postCode
					evStartDate=eventData.select("[itemprop=startDate]")[0]["content"]
					evEndDate=eventData.select("[itemprop=endDate]")[0]["content"]
					eventResults.append(EventData(evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg,eventPlace,evUrl))
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
						evName=re.sub(eliminatingStr, '', evName)
						# evDescription=eventData.select("[itemprop=description]")[0].string
						evDescription=''
						pulr=eventData.select(".product-url")
						if len(pulr)>0:evProductUrl=pulr[0].select("a")[0]["href"]
						else: evProductUrl=""
						evImg=""
						evUrl=onee.select("[itemprop=url]")[0]["href"]
						oodata,oostatus,_,_,_=connectHttpFromDomain(siteDomain,evUrl)
						ooresult=BeautifulSoup(oodata,'html.parser')
						eventImages=ooresult.find_all("div",attrs={"class": "cntImageHolder"})
						aboutBlock=ooresult.find("section",attrs={"class": "about-block"}).select("p")[0]
						for content in aboutBlock.contents:
							if content.string is not None:
								evDescription=evDescription+re.sub(eliminatingStr,'',content.string)
						if len(eventImages)>0: evImg=eventImages[0]["style"].split("url")[1][1:-2]
						# eventDate=eventData.select(".event-date")
						# if len(eventDate)>0: eventPlace=eventDate[0].string.split(',')[1].strip()
						# else: eventPlace=''
						oeventPlace=ooresult.find("div",attrs={"itemprop": "location"})
						streetAddress=oeventPlace.select("[itemprop=streetAddress]")[0].string
						locality=oeventPlace.select("[itemprop=addressLocality]")[0].string
						region=oeventPlace.select("[itemprop=addressRegion]")[0].string
						postCode=oeventPlace.select("[itemprop=postalCode]")[0].string
						eventPlace=streetAddress+' '+locality+' '+region+' '+postCode
						evStartDate=eventData.select("[itemprop=startDate]")[0]["content"]
						evEndDate=eventData.select("[itemprop=endDate]")[0]["content"]
						eventResults.append(EventData(evName,evDescription,evProductUrl,evStartDate,evEndDate,evImg,eventPlace,evUrl))
				counter+=1
	# workbook = xlsxwriter.Workbook("event/result-cityofsydney-"+month+".xlsx")
	# worksheet = workbook.add_worksheet()
	# worksheet.write(0,0,"startDate")
	# worksheet.write(0,1,"endDate")
	# worksheet.write(0,2,"name")
	# worksheet.write(0,3,"description")
	# worksheet.write(0,4,"ProductUrl")
	# worksheet.write(0,5,"Image")
	# worksheet.write(0,6,"location")
	# worksheet.write(0,7,"longitude")
	# worksheet.write(0,8,"latitude")
	# worksheet.write(0,9,"url")
	# row=1
	# for oneEv in eventResults:
		# worksheet.write(row,0,oneEv.getEvStartDate())
		# worksheet.write(row,1,oneEv.getEvEndDate())
		# worksheet.write(row,2,oneEv.getEvName())
		# worksheet.write(row,3,oneEv.getEvDescription())
		# worksheet.write(row,4,oneEv.getEvProductUrl())
		# worksheet.write(row,5,oneEv.getEvImg())
		# worksheet.write(row,9,oneEv.getEvUrl())
		# place=oneEv.getEvPlace()
		# worksheet.write(row,6,place)
		# temp=place.replace(' ','+')+'+'+country
		# tdata,tstatus,_,_,_=connectHttpFromDomain("maps.googleapis.com","/maps/api/geocode/json?address="+temp)
		# jdata=json.loads(tdata)
		# if jdata["status"]=="OK":
			# location=jdata["results"][0]["geometry"]["location"]
			# worksheet.write(row,7,location["lng"])
			# worksheet.write(row,8,location["lat"])
		# row+=1
	# workbook.close()
	with open("event/result-cityofsydney-"+month+".sql","wb") as resultSql:
		for oneEv in eventResults:
			name=oneEv.getEvName().replace("'","")
			place=oneEv.getEvPlace().replace("'","")
			description=oneEv.getEvDescription().replace("'",'')
			lng='';lat='';
			if place!='':
				temp=place.replace(' ','+')+'+'+country
				tdata,tstatus,_,_,_=connectHttpFromDomain("maps.googleapis.com","/maps/api/geocode/json?address="+temp)
				jdata=json.loads(tdata)
				if jdata["status"]=="OK":
					location=jdata["results"][0]["geometry"]["location"]
					lng=location["lng"]
					lat=location["lat"]
			try:
				resultSql.write("INSERT INTO event(startDate, endDate, name, description, location,longitude,latitude,imagePath) VALUES ('"+oneEv.getEvStartDate()+"','"+oneEv.getEvEndDate()+"','"+name+"','"+description+"','"+place+"','"+str(lng)+"','"+str(lat)+"','"+oneEv.getEvImg()+"');\n")
			except: print name