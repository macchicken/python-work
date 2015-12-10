import urllib2,urllib,json


resourceKey="&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
baseurl = "http://query.yahooapis.com/v1/public/yql?"

class FinanceResource:

	def __init__(self, currencies):
		first,second = currencies
		self.queryurl = urllib.urlencode({'q':'select * from yahoo.finance.xchange where pair in ("'+first+second+'")'})
		print 'Resource [%s]' % self.queryurl

	def __enter__(self):
		print '[Enter %s]: Allocate resource.' % self.queryurl
		self.request = baseurl + self.queryurl + resourceKey
		print "Requst %s" % self.request
		self.conn = urllib2.urlopen(self.request)
		data = json.loads(self.conn.read())
		return data
	
	def __exit__(self, exc_type, exc_value, exc_tb):
		print '[Exit %s]: Free resource.' % self.queryurl
		if exc_tb is None:
			print '[Exit %s]: Exited without exception.' % self.queryurl
			self.conn.close()
		else:
			print '[Exit %s]: Exited with exception raised.' % self.queryurl
			self.conn.close()
			return False
