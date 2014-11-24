import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import loanCalculator
import fileiopractices

class DataStorage(object):

	pPrices=[]
	fundTrade=None

	def __init__(self,unit,buyMoneyNum,rate):
		self.unit=unit
		self.buyMoneyNum=buyMoneyNum
		self.rate=rate
		self.pPrices=[price*unit for price in range(1,11)]
		fileiopractices.c.items=0
	
	def loadData(self,*parameters):
		result=[]
		for price in fileiopractices.c(self.pPrices):
			temp=loanCalculator.fundTrading(parameters[0],price,parameters[1],str(parameters[2]))
			key,value=temp[0]
			key2,value2=temp[1]
			result.append((value,value2))
		return result
	
	def setStorage(self):
		pcol=pd.Categorical(self.pPrices)
		self.fundTrade=pd.DataFrame({'Time' : pd.Timestamp('20141124'),
                        'Price' : pcol,
						'Rate(%)': np.array([self.rate] * 10,dtype='int32'),
						'subscription' : pd.Categorical(self.loadData(self.buyMoneyNum,self.rate,1)),
						'subscribe' : pd.Categorical(self.loadData(self.buyMoneyNum,self.rate,2)),
						'redemption' : pd.Categorical(self.loadData(self.buyMoneyNum,self.rate,3))},
						index=pcol)

	def load(self):
		return self.fundTrade

	def searchByIndex(self,*index):
		if (len(index)==0): return self.fundTrade.loc[[self.unit],:]
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
	
	def dataPlot(self,attr_a,attr_b):
		acol=[value for (index, value) in self.getColValues(attr_a).iteritems()]
		bcol=[value_1 for (index, (value_1,value_2)) in self.getColValues(attr_b).iteritems()]
		ccol=[value_2 for (index, (value_1,value_2)) in self.getColValues(attr_b).iteritems()]
		temp=pd.DataFrame({attr_a:acol,attr_b:bcol,'rewardmoney':ccol})
		temp.plot()
		plt.show()
	


if __name__ == '__main__':
	dataStorage=DataStorage(5,10000,3)
	dataStorage.setStorage()
	# dataStorage.sortByvalues('Price')
	# dataStorage.getColValues('Time')
	# dataStorage.searchByIndexRange(100,300,'subscribe','Time')
	# dataStorage.updateByIndex(pd.Timestamp('20141130'),'Time',100,200)
	# dataStorage.searchByIndex(100,200)
	# dataStorage.updateByPos(pd.Timestamp('20141130'),2,2)
	# dataStorage.searchByPos(0,3)
	# dataStorage.searchByCondition('>','Price',500)
	dataStorage.dataPlot('Price','redemption')
	pass
	