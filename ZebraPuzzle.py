"""
See: http://en.wikipedia.org/wiki/Zebra_Puzzle
There are five houses.
The Englishman lives in the red house.
The Spaniard owns the dog.
Coffee is drunk in the green house.
The Ukrainian drinks tea.
The green house is immediately to the right of the ivory house.
The Old Gold smoker owns snails.
Kools are smoked in the yellow house.
Milk is drunk in the middle house.
The Norwegian lives in the first house.
The man who smokes Chesterfields lives in the(a) house next to the man with the fox. 
Kools are smoked in a(the) house next to the house where the horse is kept.
The Lucky Strike smoker drinks orange juice.
The Japanese smokes Parliaments.
The Norwegian lives next to the blue house.
Now, who drinks water? Who owns the zebra? 
In the interest of clarity, it must be added that each of the five houses is painted a different color, 
and their inhabitants are of different national extractions, 
own different pets, drink different beverages and smoke different brands of American cigarets [sic]. 
One other thing: in statement 6, right means your right.

A useful method is to try to fit known relationships into a table and eliminate possibilities. 
Key deductions are in italics.
"""
#2.4GHz means processor runs 2.4 billion cycles in 1 second.
#2.4 billion instructions to get through, but we are not sure how many machine cycles it will take to do each instruction. 
#If it takes 1 cycle each, then the total run time will be 1 second, but if it takes 1000 cycles each, then it will take 1000 seconds. 
#Over time you get to have a feeling of how many cycles a piece of Python code will correspond to.
#In this example if a piece of code with 5 nest-loops,each loops go through a list of 5 element tuple of 120,
#it probably take 1 hour(3600 seconds) to run,so it can be estimated for this example that one instruction of python code roughly spends average 3600 cycles on running.  

from itertools import permutations
from time import clock
from ctypes import c_int64
from ctypes import windll
from ctypes import byref

houses=[1,2,3,4,5]#There are five houses


def memoize(f):
    cache = {}
    def helper(x):
        if x not in cache:            
            cache[x] = f(x)
        return cache[x]
    return helper

@memoize
def factorial(n):
	return 1 if n<=1 else n*factorial(n-1)
@memoize
def fib(n):
	return n if n <=1 else fib(n-1)+fib(n-2)
def fibLoop(n):
	if n<=1:return n
	else:
		prevX,prevY,result=0,1,1
		for n in range(n-1):
			prevY=result
			result+=prevX
			prevX=prevY
		return result

def assignHouseColour(houses):
	orderings=list(permutations(houses))
	return [tuple(['red-'+str(red),'green-'+str(green),'ivory-'+str(ivory),'yellow-'+str(yellow),'blue-'+str(blue)])  
			for (red,green,ivory,yellow,blue) in orderings]
def sq(x): print 'sq called', x; return x*x


def imright(h1,h2):
	"House h1 is immediately right of h2 if h1-h2 == 1."
	return h1-h2==1

def nextto(h1,h2):
	"Two houses are next to each other if they differ by 1."
	# return abs(h1-h2)==1
	return imright(h1,h2) or imright(h2,h1)

#generator expression version
def zebra_puzzle():
	"Return a tuple (ATER,ZEBRA) indicating their house numbers."
	house=first,_,middle,_,_=houses
	orderings=list(permutations(houses))
	return next(((WATER,ZEBRA)
			for (red,green,ivory,yellow,blue) in c(orderings)
			if imright(green,ivory)
			for (Englishman,Spaniard,Ukranian,Janpanese,Norwegian) in c(orderings)
			if Englishman is red and Norwegian is first and nextto(Norwegian,blue)
			for (coffee,tea,milk,oj,WATER) in c(orderings)
			if coffee is green and Ukranian is tea and milk is middle
			for (OldGold,Kools,Chesterfields,LuckyStrike,Parliaments) in c(orderings)
			if Kools is yellow and LuckyStrike is oj and Janpanese is Parliaments
			for (dog,snails,fox,horse,ZEBRA) in c(orderings)
			if Spaniard is dog
			# if Englishman is red
			# if Spaniard is dog
			# if coffee is green
			# if Ukranian is tea
			# if imright(green,ivory)
			if OldGold is snails
			# if Kools is yellow
			# if milk is middle
			# if Norwegian is first
			if nextto(Chesterfields,fox)
			if nextto(Kools,horse))
			# if LuckyStrike is oj)
			# if Janpanese is Parliaments)
			# if nextto(Norwegian,blue))
			)


def c(sequence):
	c.starts+=1
	for item in sequence:
		c.items+=1
		yield item

def instrument_fn(fn,*args):
	c.starts,c.items=0,0
	result=fn(*args)
	print '%s got %s with %5d iters over %7d items' %(fn.__name__,result,c.starts,c.items)

class instrumentDecorator(object):
	def __init__(self,fn):
		self.fn=fn
	def __call__(self,*agrs):
		c.starts,c.items=0,0
		result=self.fn(*agrs)
		print '%s got %s with %5d iters over %7d items' %(self.fn.__name__,result,c.starts,c.items)

def instrumentFnDecorator(fn):
	def new_fn(*agrs):
		c.starts,c.items=0,0
		result=fn(*agrs)
		print '%s got %s with %5d iters over %7d items' %(fn.__name__,result,c.starts,c.items)
	new_fn.__name__=fn.__name__
	return new_fn

#generator function
def ints(start,end=None):
	i=start
	while i<=end or end is None:
		yield i
		i=i+1

# def all_ints():
	# "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
	# i=0
	# while True:
		# yield i
		# if i >0:i=0-i
		# else:i=abs(i)+1
def all_ints():
	yield 0
	for i in ints(1):
		yield +i
		yield -i

def average(numbers):
	return sum(numbers)/float(len(numbers))

def timeAndCPUCyclecall(fn,*args):
	t0=clock()
	val = c_int64()
	result=fn(*args)
	windll.Kernel32.QueryPerformanceCounter(byref(val))#absolute (timing/CPU) cycle-count
	return clock()-t0,result,val.value

def timedCalls(n,fn,*args):
	"Call the function n times with args;return the min,average,and the max time."
	times=[timeAndCPUCyclecall(fn,*args)[0] for _ in range(n)]
	return min(times),average(times),max(times)

def timedCallsNew(n,fn,*args):
	#Call fn(*args) repeatedly: n times if n is an int, or up to
	#n seconds if n is a float; return the min, avg, and max time
	if isinstance(n,int):
		times=[timeAndCPUCyclecall(fn,*args)[0] for _ in range(n)]
	else:
		times=[]
		while sum(times)<n:
			times.append(timeAndCPUCyclecall(fn,*args)[0])
	return min(times),average(times),max(times)


# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

floors=[1,2,3,4,5]#There are five floors

def imHigher(fl1,fl2):
	"floor fl1 is on a higher floor than floor fl2."
	return fl1-fl2>=1

def imAdjacent(fl1,fl2):
	"floor fl1 is on a adjacent floor to floor fl2."
	return abs(fl1-fl2)==1

def floor_puzzle():
	BOTTOM,_,_,_,TOP=floors
	livings=list(permutations(floors))
	living=next(((HOPPER, KAY, LISKOV, PERLIS, RITCHIE)
				 for (HOPPER, KAY, LISKOV, PERLIS, RITCHIE) in c(livings)
					if HOPPER is not TOP and KAY is not BOTTOM
					and LISKOV is not TOP and LISKOV is not BOTTOM
					and imHigher(PERLIS,KAY) and not imAdjacent(RITCHIE,LISKOV)
					and not imAdjacent(LISKOV,KAY)))
	Hopper, Kay, Liskov, Perlis, Ritchie=living
	return  [Hopper, Kay, Liskov, Perlis, Ritchie]


# @instrumentDecorator
@instrumentFnDecorator
def floor_puzzle_decorator():
	BOTTOM,_,_,_,TOP=floors
	livings=list(permutations(floors))
	living=next(((HOPPER, KAY, LISKOV, PERLIS, RITCHIE)
				 for (HOPPER, KAY, LISKOV, PERLIS, RITCHIE) in c(livings)
					if HOPPER is not TOP and KAY is not BOTTOM
					and LISKOV is not TOP and LISKOV is not BOTTOM
					and imHigher(PERLIS,KAY) and not imAdjacent(RITCHIE,LISKOV)
					and not imAdjacent(LISKOV,KAY)))
	Hopper, Kay, Liskov, Perlis, Ritchie=living
	return  [Hopper, Kay, Liskov, Perlis, Ritchie]

if __name__ == '__main__':
	# print timeAndCPUCyclecall(factorial,50)
	# print timeAndCPUCyclecall(fib,50)
	# print timeAndCPUCyclecall(fibLoop,50)
	# print "total possibly colour assignments of houses",factorial(5)
	# print "total possibly assignments of all properties",factorial(5)**5
	# print "all combinations of five colour assignment of houses",list(permutations([1,2,3,4,5]))
	# print assignHouseColour(houses)
	# print nextto(3,2)
	# next(sq(x) for x in range(10) if x%2==0)#generator expressions
	# print zebra_puzzle()
	# for i in range(100):
		# print timeAndCPUCyclecall(zebra_puzzle)
	# print timedCalls(100,zebra_puzzle)
	# print timedCallsNew(10.0,zebra_puzzle)
	# l=ints(1)
	# next(l)
	# l=all_ints()
	# print next(l)
	# print next(l)
	# print next(l)
	# print next(l)
	# print next(l)
	# print next(l)
	# print next(l)
	# instrument_fn(zebra_puzzle)
	# instrument_fn(floor_puzzle)
	floor_puzzle_decorator()
	pass