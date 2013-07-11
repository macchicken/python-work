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



if __name__ == '__main__':
	# func1()
	# func2()
	# print func1.__name__
	pass