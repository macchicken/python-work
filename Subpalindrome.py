from os import getcwd
from re import findall
from time import clock
from ctypes import c_int64
from ctypes import windll
from ctypes import byref

def preProcess_file(filename):
	text_file=open(filename, 'r')
	text=text_file.read()
	text_file.close()
	return text

def prePorcess_text(text):
	n=len(text)
	if n==0:return ''
	else:
		text=' '.join(text.split()).lower()# remove multiple spaces from text
		#find all the words despite any others,if want all characeters to be compared,remove findall
		words=findall('[a-z]+',text)
		return '^#'+'#'.join(' '.join(words))+'#$'

def longest_subpalindrome_slice(text):
	"Return (i, j) such that text[i:j] is the longest palindrome in text."
	T = prePorcess_text(text)
	if T=='':return (0,0)
	n=len(T)
	P=[0]*n
	center_id,max_border=0,0
	for i in range(1,n-1):
		if max_border>i:P[i]=min(P[2*center_id-i],max_border-i)
		else:P[i]=0
		while T[i+1+P[i]]==T[i-1-P[i]]:P[i]+=1
		if i+P[i]>max_border:
			max_border=i+P[i]
			center_id=i
	max_len,centerIndex=0,0
	for i in range(n):
		if P[i]>max_len:
			max_len=P[i]
			centerIndex=i
	start=(centerIndex-max_len-1)/2
	end=start+max_len
	return (start,end)

def grow(text,start,end):
	#Start with a 0- or 1- length palindrome;try to grow a bigger one.
	while(start>0 and end<len(text) and text[start-1].lower()==text[end].lower()):
		start-=1;end+=1
	return (start,end)

def longest_subpalindrome_slice2(text):
	#generate candidates of longest subpalindrome by starting with each character and the next character
	if text=='':return (0,0)
	def length(slice): a,b=slice;return b-a
	candidates=[grow(text,start,end) for start in range(len(text)) for end in (start,start+1)]
	return max(candidates,key=length)

def timeAndCPUCyclecall(fn,*args):
	t0=clock()
	val = c_int64()
	result=fn(*args)
	windll.Kernel32.QueryPerformanceCounter(byref(val))#absolute (timing/CPU) cycle-count
	return clock()-t0,result,val.value

def analysisProgramInfo(fn,*args):
	timed,(start,end),cpu_cycle=timeAndCPUCyclecall(fn,*args)
	print 'total text length %d bytes' % len(*args)
	print 'start %d , end %d' % (start,end)
	print 'longest subpalindrome is:' , text[start:end]
	print 'total cpu time: %f second,overall cpu cycle: %d' % (timed,cpu_cycle)

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    print 'tests pass'




if __name__ == '__main__':
	# print prePorcess_text('ab ba')
	# print longest_subpalindrome_slice('racecar')
	test()
	# text = preProcess_file(getcwd()+'\\War_and_Peace.txt')
	# analysisProgramInfo(longest_subpalindrome_slice2,text)
	# analysisProgramInfo(longest_subpalindrome_slice,text)
	pass