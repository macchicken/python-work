# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The 
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is 
# efficient enough. 


def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1

def newtons_inverse(f, delta =  0.00001):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def d(f, eps=0.00001): return lambda x: (f(x+eps)-f(x))/eps
    def f_i(y):
        x=10
        df=d(f)
        while abs(f(x)-y)>delta: x=x-(f(x)-y)/df(x)
        return x
    return f_i

def binarysearch_inverse(f, delta = 1/1024.):
    def f_1(y):
        lo, hi = find_bounds(f, y)
        return binary_search(f, y, lo, hi, delta)
    return f_1

def find_bounds(f, y):
    x = 1
    while f(x) < y:
        x *= 2.
    lo = 0 if (x == 1) else x/2
    return lo, x

def binary_search(f, y, lo, hi, delta):
    while lo <= hi:
        x = (lo + hi) / 2.
        if f(x) < y:
            lo = x + delta
        elif f(x) > y:
            hi = x - delta
        else:
            return x
    return hi if (f(hi)-y < y-f(lo)) else lo

def square(x): return x*x

def power10(x): return 10**x


def test():
    import math
    nums = [2, 4, 6, 8, 10, 25, 100, 101, 1000, 10000, 20000, 40000, 100000000]
    sqrt=newtons_inverse(square)
    log10=newtons_inverse(power10)
    cuberoot=newtons_inverse(lambda x: x*x*x)
    for n in nums:
        test1(n, 'sqrt', sqrt(n), math.sqrt(n))
        test1(n, 'log', log10(n), math.log10(n))
        test1(n, '3-rt', cuberoot(n), n**(1./3.))

def test1(n, name, value, expected):
    diff = abs(value - expected)
    print '%6g: %s = %13.7f (%13.7f actual); %.4f diff; %s' % (
        n, name, value, expected, diff, ('ok' if diff < .002 else 'BAD'))

def test_time():
    nums = [2, 4, 6, 8, 10, 100, 101, 1000, 10000, 20000, 40000, 100000000]
    sqrt=newtons_inverse(square)
    log10=newtons_inverse(power10)
    cuberoot=newtons_inverse(lambda x: x*x*x)
    for n in nums:
        sqrt(n), log10(n), cuberoot(n)

def test_profile():
	import cProfile
	print 'sqaure root -------------'
	cProfile.run('sqrt(1000000000)')
	cProfile.run('sqrt2(1000000000)')
	cProfile.run('sqrt3(1000000000)')
	
	print 'log 10 ------------------'
	cProfile.run('log10(1000000000)')
	cProfile.run('log10_2(1000000000)')
	cProfile.run('log10_3(1000000000)')
	
	print 'cube root ---------------'
	cProfile.run('cuberoot(1000000000)')
	cProfile.run('cuberoot2(1000000000)')
	cProfile.run('cuberoot3(1000000000)')
	
if __name__ == '__main__':
	# sqrt = slow_inverse(square)
	# sqrt2 = newtons_inverse(square)
	# sqrt3 = binarysearch_inverse(square)
	
	# log10 = slow_inverse(power10)
	# log10_2 = newtons_inverse(power10)
	# log10_3 = binarysearch_inverse(power10)
	
	# cuberoot=slow_inverse(lambda x: x*x*x)
	# cuberoot2=newtons_inverse(lambda x: x*x*x)
	# cuberoot3=binarysearch_inverse(lambda x: x*x*x)
	
	# test_profile()
	test()
	# import cProfile
	# cProfile.run('test_time()')