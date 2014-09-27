from datetime import date
from datetime import timedelta

weekdayMapping={1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}

def calWorkingDates(beginDay=date.today(),endDay=date.today()):
	workingDatesCount=0
	holidays,specialworkingDays=readInholidays()
	workingDates=[]
	while(beginDay<=endDay):
		if (str(beginDay) not in holidays):
			if (str(beginDay) in specialworkingDays):
				workingDatesCount+=1;workingDates.append(str(beginDay)+" "+weekdayMapping[weekday])
			else:
				weekday=beginDay.isoweekday()
				if (weekday!=6 and weekday!=7):#is not sat and sunday
					workingDatesCount+=1;workingDates.append(str(beginDay)+" "+weekdayMapping[weekday])
		beginDay+=timedelta(days=1)
	return workingDatesCount,workingDates

def readInholidays():
	with open("D:\\hc105\\python-work\\testdata\\holidays.txt","rb") as txtFile:
		holidays=[];specialworkingDays=[]
		hf=False;wf=False
		for line in txtFile:
			if line=="holidays:\n": hf=True;wf=False
			elif line=="workingDays:\n": hf=False;wf=True
			elif hf: holidays.append(line.replace('\n',''))
			elif wf: specialworkingDays.append(line.replace('\n',''))
	return holidays,specialworkingDays

if __name__ == '__main__':
  workingDatesCount,workingDates=calWorkingDates(beginDay=date(2014,9,16))
  print "sum of working days: "+str(workingDatesCount)
  print workingDates
