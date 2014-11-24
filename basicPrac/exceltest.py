import xdrlib ,sys
import xlrd
from chardet.universaldetector import UniversalDetector


class Question(object):
	def __init__(self, qname, answer, choices):
		self.qname = qname
		self.answer = answer
		self.choices = choices
	def setChoices(self,choices):
		self.choices=self.choices+choices


def open_excel(file='C:\\Users\\Barry\\Desktop\\1.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
def excel_table_byindex(file='C:\\Users\\Barry\\Desktop\\1.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    colnames = table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
             list.append(app)
    return list

def excel_table_byname(file='C:\\Users\\Barry\\Desktop\\1.xls',colnameindex=0,by_name='design'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows
    colnames =  table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def excel_table_byindex2(file='C:\\Users\\Barry\\Desktop\\1.xls',colnameindex=0,by_index=0):
	book = open_excel(file)
	onesheet = book.sheets()[by_index]
	nrows = onesheet.nrows
	ncols = onesheet.ncols
	colnames = onesheet.row_values(colnameindex)
	list =[]
	count=0
	qname=''
	answer=''
	choices=''
	for rownum in range(1,nrows):
		row = onesheet.row_values(rownum)
		count+=1
		if row:
			if (type(row[0]) is float):
				list.append(Question(qname,answer,choices))
				qname=''
				answer=''
				choices=''
			if (len(row)>11):
				if (row[4]!=''): qname=row[4]
				if (row[6]!=''): answer=row[6]
				if (type(row[12]) is float): temp=str(row[12])
				else: temp=row[12]
				choices=choices+row[11]+temp+'\n'
	list.append(Question(qname,answer,choices))
	return list

def main():
   # tables = excel_table_byindex()
   # for row in tables:
       # print row
   # tables = excel_table_byname()
   # for row in tables:
       # print row
   qlist=excel_table_byindex2('C:\\Users\\Barry\\Desktop\\JAVA20140916.xls')
   detector = UniversalDetector()
   for q in qlist:
	detector.reset()
	if q.qname!='':
		detector.feed(q.choices)
		detector.close()
		print detector.result["encoding"]
		# print q.choices
		# print q.qname
	detector.close()


if __name__=="__main__":
    main()
