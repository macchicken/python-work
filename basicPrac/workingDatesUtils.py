from datetime import date
from datetime import timedelta

weekdayMapping={1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
daySalary=300

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
  dateStr=raw_input("working date begin at for this month(yyyy-mm-dd)").replace(' ','').split('-')
  workingDatesCount,workingDates=calWorkingDates(beginDay=date(int(dateStr[0]),int(dateStr[1]),int(dateStr[2])))
  offdays=eval(raw_input("day off"))
  print "sum of expected working days: "+str(workingDatesCount)
  print workingDates
  print "total salary of current month: "+str((workingDatesCount-offdays)*daySalary)
