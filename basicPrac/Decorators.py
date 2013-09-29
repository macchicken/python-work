from functools import update_wrapper


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


# ---------------
# User Instructions
#
# Write a function, n_ary(f), that takes a binary function (a function
# that takes 2 inputs) as input and returns an n_ary function. 

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


if __name__ == '__main__':
	# func1()
	# func2()
	# print func1.__name__
	print seq('a','a','a')
	print "help message "
	help(seq)
	pass