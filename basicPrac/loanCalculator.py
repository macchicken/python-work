 # coding=GBK
import math
import decimal

# from CCB CHINA CONSTRUCTION BANK
"""
monthInterest 每月应付利息
monthBack 每月支付本息
totalInterest 累计支付利息
totalBack 累计还款总额

original 贷款金额
active 贷款利率(年利率)
yearSpan 详细期限(年)
"""
thousandth=decimal.Decimal(0.001)
one=decimal.Decimal('1')
hundred=decimal.Decimal('100')
thousand=decimal.Decimal('1000')
tenthousand=decimal.Decimal('10000')


#等额本息还款
def estateBorrow(original,active,yearSpan):
	timeSpan=yearSpan*12
	monthBack=original*active*thousandth*decimal.Decimal(math.pow((one+(active*thousandth)),timeSpan))/(decimal.Decimal(math.pow((one+active*thousandth),timeSpan))-one)
	totalBack=monthBack*decimal.Decimal(str(timeSpan))
	totalInterest=totalBack-original
	monthInterest=totalInterest/decimal.Decimal(str(timeSpan))
	totalInterest=(round(totalInterest*hundred))/100
	monthInterest=(round(monthInterest*tenthousand))/10000
	monthBack=(round(monthBack*tenthousand))/10000
	totalBack=(round(totalBack*hundred))/100
	return [("等额本息还款",":"),("每月应付利息",monthBack),("累计还款总额",totalBack),("每月应付利息",monthInterest),("累计支付利息",totalInterest)]

#等额本金还款
def estateBorrow1(original,active,yearSpan):
	timeSpan=yearSpan*12
	timeSpan1=int(timeSpan)
	interestTotal=decimal.Decimal('0')
	for i in range(1,timeSpan1+1):
		interestM=(original-original*decimal.Decimal(i-1)/decimal.Decimal(str(timeSpan1)))*active*thousandth
		interestTotal=interestTotal+interestM
	monthBack=original*active*thousandth*decimal.Decimal(math.pow((one+active*thousandth),timeSpan))/(decimal.Decimal(math.pow((one+active*thousandth),timeSpan))-one)
	interestTotal=round(interestTotal*hundred)/100
	moneyTotal=float(original)+interestTotal
	return [("等额本金还款",":"),("累计支付利息",interestTotal),("累计还款总额",moneyTotal)]

def main():
	original=raw_input("贷款金额")
	yearSpan=raw_input("详细期限(年)")
	active=raw_input("贷款利率(年利率)%")
	paymentMethod=raw_input("还款方式(1-等额本息还款 2-等额本金还款 other-both)")
	original=decimal.Decimal('%.15f'%float(original))
	active=decimal.Decimal('%.15f'%(float(active)*10/12))
	yearSpan=int(yearSpan)
	if paymentMethod=="1":
		result=estateBorrow(original,active,yearSpan)
	elif paymentMethod=="2":
		result=estateBorrow1(original,active,yearSpan)
	else:
		result=estateBorrow(original,active,yearSpan)
		result+=estateBorrow1(original,active,yearSpan)
	for key,value in result: print key,value


if __name__ == '__main__':
	main()
