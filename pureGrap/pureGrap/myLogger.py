import datetime,traceback,sys,threading,Queue,logging


def logEntry(f):
	def new_f(*args):
		print "arguments: {}".format(', '.join(map(repr, args)))
		return f(*args)
	return new_f

def writeLog(logFile,mode="ab"):
	with open(logFile,mode) as t:
		t.write(("\n%s\n" %(datetime.datetime.now())))
		traceback.print_exc(file=t)

def logToConsole():
	traceback.print_exc(file=sys.stdout)

class AsyncLogger(threading.Thread):

	def __init__(self,logFile):
		self._queue=Queue.Queue()
		self.logFile=logFile
		threading.Thread.__init__(self)
		self.daemon=True
		self.start()

	def run(self):
		while True:
			(record,flag)=self._queue.get(True)
			if flag==1: print record
			else:
				with open(self.logFile,"ab") as t:
					t.write(("\n%s\n%s" %(datetime.datetime.now(),record)))

	def logToConsole(self):
		record=traceback.format_exc()
		self._queue.put((record,1))
	
	def logToFile(self):
		record=traceback.format_exc()
		self._queue.put((record,2))

class AsyncLogging(threading.Thread):
	
	def __init__(self,appName,logFile):
		self._queue=Queue.Queue()
		logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename=logFile,filemode='ab')
		self.logger=logging.getLogger(appName)
		self.console=logging.getLogger(appName+"-Console")
		self.console.addHandler(logging.StreamHandler())
		threading.Thread.__init__(self)
		self.daemon=True
		self.start()

	def run(self):
		while True:
			(logLevel,record,flag)=self._queue.get(True)
			if flag==1: self.console.debug(record)
			else: self.logger.debug(record)

	def logToConsole(self,logLevel):
		record=traceback.format_exc()
		self._queue.put((logLevel,record,1))

	def logToFile(self,logLevel):
		record=traceback.format_exc()
		self._queue.put((logLevel,record,2))
	
	def logMessageToFile(self,message,logLevel):
		record=traceback.format_exc()
		self._queue.put((logLevel,message+"\n"+record,2))

class recordTimeElapse():
	
	def __init__(self):
		self.startTime=datetime.datetime.now()
		
	def __enter__(self):
		print "start at {}".format(self.startTime)
	
	def __exit__(self,type,vale,traceback):
		print "total time spent {}".format(datetime.datetime.now()-self.startTime)