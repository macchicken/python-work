from datetime import date
from datetime import timedelta
from os import getcwd
from string import replace
from re import match

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
       ms=match('[0]+',str)
       if ms is not None:
          return int(str[ms.end():])
       else:
          return int(str)
    else:
        return 0

def isValidMathNumber(str):
    if not str.isdigit():
        result = match(('[0-9]+[.][0-9]+'),str)
        if result is not None:
            return result.end()==len(str)
        else:
            return False
    else:
        return True

def testFileIO():
    read_file = open(getcwd()+"\\currtask.txt",'r')
    try:
        temp=[]
        count=0
        tempint=''
        for line in read_file:
            if isNotEmptyStr(line):
                temp=line.split()
                if len(temp)>0:
                    tempint=trim(replace(temp[len(temp)-2],',',''))
                    if isValidMathNumber(tempint):
                        count+=parseStrToInt(tempint)
                    tempint=''
                    temp=[]
    finally:
        read_file.close()
    return count
if __name__ == '__main__':
    print testFileIO()
