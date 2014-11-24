from datetime import date
from datetime import timedelta
from os import getcwd
from string import replace
import re


dbt={}

class sysServie(object):
	def __init__(self, pname, mem, pid):
		self.pname = pname
		self.mem = mem
		self.pid = pid
	def getPname(self):
		return self.pname
	def getMen(self):
		return self.mem
	def getPid(self):
		return self.pid
	def __repr__(self):
		return self.pname+' memory '+self.mem+' pid '+self.pid
	
def putData(key,value):
	try:
		old=dbt[key]
	except KeyError:
		old=[]
	old.append(value)
	dbt[key]=old
	
def trim(str):
    return replace(str,' ','')

def isNotEmptyStr(str):
    return (str is not None and len(trim(str))>0)

def testDate():    
    date1 = date(2010,7,29)
    date2 = date(2013,5,24)
    timedelta = date2-date1
    print "differences between two date is:",timedelta
    print "total number of seconds is: ",timedelta.total_seconds()

def parseStrToInt(str):
	if isNotEmptyStr(str):
		ms=re.match('[0]+',str)
		if ms is not None:
			return int(str[ms.end():])
		else:
			return int(str)
	else:
		return 0

def isValidMathNumber(str):
    if not str.isdigit():
        result = re.match(('[0-9]+[.][0-9]+'),str)
        if result is not None:
            return result.end()==len(str)
        else:
            return False
    else:
        return True

def getMemoryUsage():
	read_file = open(getcwd()+"\\currtask.txt",'r')
	try:
		count=0
		for line in read_file:
			if isNotEmptyStr(line):
				temp=line.split()
				if len(temp)>0:
					tempint=trim(replace(temp[len(temp)-2],',',''))
					if isValidMathNumber(tempint):
						count+=parseStrToInt(tempint)
	finally:
		read_file.close()
	return count

def groupInConversation(skip=3):
	linenum=0
	with open(getcwd()+"\\currtask.txt",'r') as read_file:
		for line in read_file:
			if linenum>=skip and isNotEmptyStr(line):
				mResult=re.findall(r'.+',line)
				data=line.split()
				process=sysServie(data[0],data[4],data[1])
				putData(data[2],process)
			linenum+=1


if __name__ == '__main__':
    # print str(getMemoryUsage())+"K"
	groupInConversation()
	print dbt['Services']
