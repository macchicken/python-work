# from __future__ import division
import string, re
from itertools import permutations
from itertools import izip
from time import clock

#String literals may optionally be prefixed with a letter 'r' or 'R'; such strings are called
#raw strings and use different rules for interpreting backslash escape sequences
#Raw String Notation (r"text")
#Without it, every backslash ('\') in a regular expression would
#have to be prefixed with another one to escape it (see http://docs.python.org/2.7/library/re.html)
#https://developers.google.com/edu/python/regular-expressions?hl=zh-CN#
#analysis performance of a python script python -m cProfile Cryptarithmetic.py

def solve(formula):
	"""Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
	Input formula is a string; output is a digit-filled-in string or None."""
	try:
		f=fill_in(formula)
		result=next(f)
		while not valid(result):
			result=next(f)
		return result
	except StopIteration:
		return None
	# try:
		# return next(result for result in fill_in(formula) if valid(result))
	# except StopIteration:
		# return None
	# for result in fill_in(formula):
		# if valid(result):
			# return result

def solveAllValues(formula):
	return [result for result in fill_in(formula) if valid(result)]
	#for-loop call next() of the iterable object in each iteration and return a result elment

def fill_in(formula):
	"Generate all possible fillings-in of letters in formula with digits."
	letters=''.join((set(re.findall(r'[A-Z]',formula))))
	#for-loop call next() of the iterable object in each iteration and return a result elment
	for numbers in permutations('0123456789',len(letters)):
		table=string.maketrans(letters,''.join(numbers))
		yield formula.translate(table)

def valid(f):
    "Formula f is valid iff it has no numbers with leading zero and evals true."
    try:
		return not re.search(r'\b0[0-9]',f) and eval(f) is True
		# return not re.search('\\b0[0-9]',f) and eval(f) is True
    except ArithmeticError:
		print "ArithmeticError"
		return False

def compile_word(word):
	"""Compile a word of uppercase letters as numeric digits.
	E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
	Non-uppercase words unchanged: compile_word('+') => '+'"""
	if not word.isupper():
		return word
	else:
		result=[]
		i=len(word)
		for c in word:
			i-=1
			result.append(str(10**i)+'*'+c)
		return '('+'+'.join(result)+')'
	# if word.isupper():
		# terms=[('%s*%s' % (10**i,d)) for (i,d) in enumerate(word[::-1])]
		# return '('+'+'.join(terms)+')'
	# else:
		# return word

def compile_word_new(word):
	"""Compile a word of uppercase letters as numeric digits.
	E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
	Non-uppercase words unchanged: compile_word('+') => '+'"""
	if not word.isupper():
		return ''
	else:
		result=[]
		i=len(word)
		for c in word:
			i-=1
			result.append(str(10**i)+'*'+c)
		return '+'.join(result)

	
def compile_formula(formula,verbose=False):
	#Compile formual into a lambda function.Also return letters found,as a str,
	# in same order as parms of function. For example,'YOU==ME***2' returns
	#(lambda Y,M,E,U,O:(U+10*O+100*Y)==(E+10*M)**2,'YMEUO'
	letters=''.join(set(re.findall(r'[A-Z]',formula)))
	parms=','.join(letters)
	tokens=map(compile_word,re.split('([A-Z]+)',formula))
	body=''.join(tokens)
	f='lambda %s: %s' % (parms,body)
	if verbose:print f
	return eval(f),letters

def compile_formula_to_func(formula,verbose=False):
	#Compile formual into a function.Also return letters found,as a str,
	# in same order as parms of function. For example,'YOU==ME***2' returns
	#(lambda Y,M,E,U,O:(U+10*O+100*Y)==(E+10*M)**2,'YMEUO'
	letters=''.join(set(re.findall(r'[A-Z]',formula)))
	parms=','.join(letters)
	token_list=re.split('([A-Z]+)',formula)
	tokens=map(compile_word_new,token_list)
	functions_logic=''
	for (x,y) in list(set(izip(token_list,tokens))):
		if x!='' and y!='':
			functions_logic+=x+'=('+y+')\n\t'
	return_statment='return '+''.join(token_list)
	body=functions_logic+return_statment
	func='def checker(%s):\n\t%s' % (parms,body)
	if verbose:print func
	return func,letters

def compile_formula_modify(formula,verbose=False):
	"""Compile formula into a function. Also return letters found, as a str,
	in same order as parms of function. The first digit of a multi-digit 
	number can't be 0. So if YOU is a word in the formula, and the function
	is called with Y eqal to 0, the function should return False."""
	letters=''.join(set(re.findall(r'[A-Z]',formula)))
	parms=','.join(letters)
	token_list=re.split('([A-Z]+)',formula)
	start_of_letters=''.join(list(set([word[0] for word in token_list if word.isupper()])))
	tokens=map(compile_word,token_list)
	body=''.join(tokens)
	if start_of_letters!='':
		body=' '.join([c+'!=0 and' for c in start_of_letters])+' '+body
	f='lambda %s: %s' % (parms,body)
	if verbose:print f
	return eval(f),letters

def compile_formula_modify2(formula,verbose=False):
	letters=''.join(set(re.findall(r'[A-Z]',formula)))
	first_letters=set(re.findall(r'\b([A-Z])[A-Z]',formula))
	parms=','.join(letters)
	tokens=map(compile_word,re.split('([A-Z]+)',formula))
	body=''.join(tokens)
	if first_letters:
		tests=' and '.join(l+'!=0' for l in first_letters)
		body='%s and (%s)' % (tests,body)
	f='lambda %s: %s' % (parms,body)
	if verbose:print f
	return eval(f),letters

def faster_solve(formula):
	#this version precompiles the formula;only one eval per formula.
	# f,letters=compile_formula(formula,True)
	# f,letters=compile_formula_modify2(formula,True)
	f,letters=compile_formula_modify(formula,True)
	for digits in permutations((0,1,2,3,4,5,6,7,8,9),len(letters)):
		try:
			if f(*digits) is True:
				table=string.maketrans(letters,''.join(map(str,digits)))
				return formula.translate(table)
		except ArithmeticError:
			pass


examples="""TWO+TWO==FOUR\nA**2+B**2==C**2\nA**2+BE**2==BY**2
X/X==X\nA**N+B**N==C**N and N>1\nATOM**0.5==A+TO+M
GILLTERS is not GLOD\nONE<TWO and FOUR<FIVE\nONE<TWO<THREE
RAMN==R**3+RM**3==N**3+RX**3\nsum(range(AA))==BB\nsum(range(POP))==BOBO
ODD+ODD==EVEN\nPLUTO not in set([PLANETS])""".splitlines()

def timedcall(fn,*args):
	t0=clock()
	result=fn(*args)
	return clock()-t0,result

def test():
	t0=clock()
	for example in examples:
		print;print 13*'',example
		print '%6.4f sec:	%s ' % timedcall(solve,example)
		# timed,result=timedcall(solveAllValues,example)
		# print '%6.4f sec with total %d solves' % (timed,len(result))
	print '%6.4f total.' % (clock()-t0)





if __name__ == '__main__':
	# print valid('1+2==3')
	# table=string.maketrans('NEDOV','12345')
	# print 'ODD+ODD=EVEN'.translate(table)
	# letters=''.join(set(re.findall(r'[a-zA-Z]','ODD+ODD=EVEN')))
	# print letters
	# print solve('ODD+ODD==EVEN')
	# print solveAllValues('ODD+ODD==EVEN')
	# print test()
	# print compile_word('YOU')
	# print map(str,(1,2,3))
	# print re.split('([A-Z]+)','ODD+ODD==EVEN')
	# print faster_solve('ODD+ODD==EVEN')
	# compile_formula_modify2('YOU==ME**2',True)
	# func,letters=compile_formula_to_func('YOU==ME**2',True)
	# code_obj=compile(func,'<string>','single')
	# exec(code_obj,None,{'Y':1,'M':2,'E':3,'U':4,'O':5})
	# print re.findall(r'\b([A-Z])','YOU==ME**2')
	pass
