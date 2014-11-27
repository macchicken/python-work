import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import loanCalculator
import fileiopractices
import datetime

class DataStorage(object):

	pBMN=[]
	fundTrade=None

	def __init__(self,buyMoneyNum,price,rate):
		self.buyMoneyNum=buyMoneyNum
		self.rate=rate
		self.price=price
		self.pBMN=[buyMoneyNum*unit for unit in range(1,11)]
		self.middle=self.pBMN[len(self.pBMN)/2]
		fileiopractices.c.items=0

	def loadData(self,*parameters):
		ts=[tuple(loanCalculator.fundTrading(bmn,parameters[0],parameters[1],str(parameters[2]))) if bmn<=self.middle else tuple(loanCalculator.fundTrading(bmn,parameters[0],parameters[1]/3,str(parameters[2]))) for bmn in fileiopractices.c(self.pBMN)]
		return [(v,v2) for (k,v),(k2,v2) in ts]
	
	def setStorage(self,stime=datetime.datetime.now()):
		stime=datetime.datetime(stime.year,stime.month,stime.day,stime.hour)
		pcol=pd.Categorical(self.pBMN)
		self.fundTrade=pd.DataFrame({'Time' : pd.Timestamp(stime),
                        'buyMoneyNumber' : pcol,
						'Rate': np.array([self.rate]*(len(self.pBMN)/2)+[self.rate/3]*(len(self.pBMN)-(len(self.pBMN)/2)),dtype='float32'),
						'subscription' : pd.Categorical(self.loadData(self.price,self.rate,1)),
						'subscribe' : pd.Categorical(self.loadData(self.price,self.rate,2)),
						'redemption' : pd.Categorical(self.loadData(self.price,self.rate,3))},
						index=pcol)

	def load(self):
		return self.fundTrade

	def searchByIndex(self,*index):
		if (len(index)==0): return self.fundTrade.loc[[self.buyMoneyNum],:]
		else: 
			return self.fundTrade.loc[index,:]
	def searchByPos(self,start,end=None):
		if start<0:start=0
		if end==None: return self.fundTrade.iloc[start]
		else: return self.fundTrade.iloc[start:end]
	def searchByIndexRange(self,start,end,*columnNames):
		if len(columnNames)!=0: return self.fundTrade.loc[start:end,columnNames]
		else: return self.fundTrade[start:end]
	def searchByCondition(self,operator,col,value):
		if operator=='>': return self.fundTrade[self.fundTrade[col] > value]
		elif operator=='<': return self.fundTrade[self.fundTrade[col] < value]
		else: return self.fundTrade[self.fundTrade[col] == value]
	
	def transport(self):
		return self.fundTrade.T
	def StatsSummary(self):
		return self.fundTrade.describe()
	def sortByvalues(self,column,ascend=False):
		return self.fundTrade.sort(columns=column,ascending=ascend)
	def getColValues(self,columnName):
		return self.fundTrade[columnName]
	
	def updateByIndex(self,value,columnName,start,end=None):
		if end is not None: result=self.fundTrade.at[start:end,columnName]=value
		else: result=self.fundTrade.at[start,columnName]=value
		return result
	def updateByPos(self,value,start,colindex):
		result=self.fundTrade.iat[start,colindex]=value
		return result
	
	def dataPlot(self,attr_a,attr_b,scale=1000):
		if attr_b!='redemption': scale=1
		acol=[value/scale for (index, value) in self.getColValues(attr_a).iteritems()]
		bcol=[value_1/scale for (index, (value_1,value_2)) in self.getColValues(attr_b).iteritems()]
		ccol=[value_2/scale for (index, (value_1,value_2)) in self.getColValues(attr_b).iteritems()]
		temp=pd.DataFrame({attr_b+'('+str(scale)+')':bcol,'rewardmoney('+str(scale)+')':ccol},index=acol)
		temp2=pd.DataFrame({'rewardmoney('+str(scale)+')':ccol},index=bcol)
		temp.plot()
		temp2.plot()
		plt.show()



if __name__ == '__main__':
	dataStorage=DataStorage(10000,100,1.5)
	dataStorage.setStorage()
	# print dataStorage.load()
	# dataStorage.sortByvalues('buyMoneyNumber')
	# dataStorage.getColValues('Time')
	# dataStorage.searchByIndexRange(100,300,'subscribe','Time')
	# dataStorage.updateByIndex(pd.Timestamp('20141130'),'Time',100,200)
	# dataStorage.searchByIndex(100,200)
	# dataStorage.updateByPos(pd.Timestamp('20141130'),2,2)
	# dataStorage.searchByPos(0,3)
	# dataStorage.searchByCondition('>','buyMoneyNumber',500)
	dataStorage.dataPlot('buyMoneyNumber','redemption')
	pass
	