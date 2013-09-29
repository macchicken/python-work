from functools import update_wrapper
from decimal import Decimal

class clentryExit(object):
    def __init__(self, f):
		print 'clentryExit init'
		self.f = f
    def __call__(self):
        print "Entering", self.f.__name__
        self.f()
        print "Exited", self.f.__name__

def entryExit(f):
	print 'entryExit defined'
	def new_f():
		print "Entering", f.__name__
		f()
		print "Exited", f.__name__
	return new_f


@entryExit
def func1():
    print "inside func1()"

@entryExit
def func2():
    print "inside func2()"


# ------------------------------


def decorator(d):
	"Make function d a decorator: d wraps a function."
	def _d(fn): return update_wrapper(d(fn),fn);
	update_wrapper(_d,d);
	return _d

def bacon_decorator(d): return lambda fn: update_wrapper(d(fn),fn)
bacon_decorator=bacon_decorator(bacon_decorator)

# @decorator
@bacon_decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args): return x if not args else f(x,n_ary_f(*args))
    return n_ary_f

@n_ary
def seq(x,y): return ('seq',x,y)

@decorator
def memo(f):
	"""Decorator that caches the return value for each call to f(args).
	Then when called again with same args,we can just look it up."""
	cache={}
	def _f(*args):
		try:
			return cache[args]
		except KeyError:
			cache[args]=result=f(*args)
			return cache[args]
		except TypeError:
			return f(args)
	return _f

callcounts={}
@decorator
def countcalls(f):
	"Decorator that makes the funciton count callss to it,it callcounts[f]."
	def _f(*args):
		callcounts[_f]+=1
		return f(*args)
	callcounts[_f]=0
	return _f

@decorator
def trace(f):
    indent='   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level+=1
        try:
            result=f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent,signature, result)
        finally:
            trace.level-=1
        return result
    trace.level=0
    return _f

def disabled(f): return f

def print_statistic(f):
	print "n	%s(n)	calls	call raio" % (f.__name__)
	calls=None
	prev_calls=Decimal(1.0000)
	for i in range(31):
		result=f(i)
		calls=callcounts.values()[0]
		print str(i)+"	"+str(result)+"	"+str(calls)+"	"+str(round(Decimal(calls)/prev_calls,4))
		prev_calls=Decimal(calls)


@countcalls
@memo
@trace
def fib(n): return 1 if n<=1 else fib(n-1)+fib(n-2)


if __name__ == '__main__':
	# func1()
	# func2()
	# print func1.__name__
	print seq('a','a','a')
	print "help message "
	help(seq)
	# print_statistic(fib)
	fib(6)
	pass