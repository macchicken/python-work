 # coding=GBK
import math
import decimal

# from CCB CHINA CONSTRUCTION BANK
"""
monthInterest ÿ��Ӧ����Ϣ
monthBack ÿ��֧����Ϣ
totalInterest �ۼ�֧����Ϣ
totalBack �ۼƻ����ܶ�

original ������
active ��������(������)
yearSpan ��ϸ����(��)
"""
thousandth=decimal.Decimal(0.001)
one=decimal.Decimal('1')
hundred=decimal.Decimal('100')
thousand=decimal.Decimal('1000')
tenthousand=decimal.Decimal('10000')


#�ȶϢ����
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
	return [("�ȶϢ����",":"),("ÿ��Ӧ����Ϣ",monthBack),("�ۼƻ����ܶ�",totalBack),("ÿ��Ӧ����Ϣ",monthInterest),("�ۼ�֧����Ϣ",totalInterest)]

#�ȶ�𻹿�
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
	return [("�ȶ�𻹿�",":"),("�ۼ�֧����Ϣ",interestTotal),("�ۼƻ����ܶ�",moneyTotal)]

def main():
	original=raw_input("������")
	yearSpan=raw_input("��ϸ����(��)")
	active=raw_input("��������(������)%")
	paymentMethod=raw_input("���ʽ(1-�ȶϢ���� 2-�ȶ�𻹿� other-both)")
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
