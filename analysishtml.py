# python -m profile analysishtml.py---display the program profiling data after running
from HTMLParser import HTMLParser
from os import getcwd
# from htmlentitydefs import name2codepoint

# create a subclass and override the handler methods
class NetEaseHTMLParser(HTMLParser):
	
	containPhoto=False
	containImg=False
	result=[]

	def handle_starttag(self, tag, attrs):
		# print "Start tag:", tag
		# print 'attrs',attrs
		if tag=='textarea' and (('id','photoList') in attrs):
			self.containPhoto=True
		if ('title','img') in attrs:
			self.containImg=True
		else:self.containImg=False
		# pass
	def handle_endtag(self, tag):
		# print "End tag  :", tag
		if tag=='textarea' and self.containPhoto:
			self.containPhoto=False
		# pass
	def handle_data(self, data):
		# print "Data     :", data
		if self.containPhoto and self.containImg and 'http://' in data:
			self.result.append(data)
		# pass
	def handle_comment(self, data):
        # print "Comment  :", data
		pass
	def handle_entityref(self, name):
		# c = unichr(name2codepoint[name])
		# print "Named ent:", c
		pass
	def handle_charref(self, name):
        # if name.startswith('x'):
            # c = unichr(int(name[1:], 16))
        # else:
            # c = unichr(int(name))
        # print "Num ent  :", c
		pass
	def handle_decl(self, data):
		# print "Decl     :", data
		pass
	def getResult(self):
		return self.result

class yahooHTMLParse(HTMLParser):
	
	scriptText=False
	result=None

	def handle_starttag(self, tag, attrs):
		# print "Start tag:", tag
		# print 'attrs',attrs
		if tag=='script' and attrs==[('type', 'text/javascript')]:
			self.scriptText=True
		# pass
	def handle_endtag(self, tag):
		# print "End tag  :", tag
		if tag=='script':
			self.scriptText=False
		# pass
	def handle_data(self, data):
		# print "Data     :", data
		if self.scriptText and data.find('var data=')==1:
			self.result=data.split(';')[0].replace('\n','').replace('var data= ','')
		# pass
	def getResult(self):
		return self.result

class MsnHTMLParser(HTMLParser):
	
	photoList=False
	result=[]

	def handle_starttag(self, tag, attrs):
		# print "Start tag:", tag
		# print 'attrs',attrs
		if tag=='div' and attrs==[('id', 'photolist')]:
			self.photoList=True
		if self.photoList and tag=='img':
			(_,values)=attrs[2]
			self.result.append(values)
		# pass
	def handle_endtag(self, tag):
		# print "End tag  :", tag
		if tag=='div':
			self.photoList=False
		# pass
	def handle_data(self, data):
		# print "Data     :", data
		pass
	def getResult(self):
		return self.result

def parseNetEaseHTML():
	# instantiate the parser and fed it some HTML
	parser = NetEaseHTMLParser()
	htmlfile = open(getcwd()+"\\92AVGGVA00314K8H.txt", "r")
	parser.feed(htmlfile.read())
	parser.close()
	htmlfile.close()
	result=parser.getResult()
	target = open(getcwd()+"\\digi163galleryData.txt", "wb")
	for data in result:
		target.write(data+'\n')
	target.close()
	print 'done'

def parseYahooHTML():
	parser = yahooHTMLParse()
	htmlfile = open(getcwd()+"\\34545.txt", "r")
	parser.feed(htmlfile.read())
	parser.close()
	htmlfile.close()
	result=parser.getResult()
	target = open(getcwd()+"\\yahooPicData.txt", "wb")
	target.write(result)
	target.close()
	print 'done'

def parseMsnHTML():
	parser = MsnHTMLParser()
	htmlfile = open(getcwd()+"\\msnhtml.txt", "r")
	parser.feed(htmlfile.read())
	parser.close()
	htmlfile.close()
	result=parser.getResult()
	target = open(getcwd()+"\\msnPicData.txt", "wb")
	for urlAddress in result:
		target.write(urlAddress+'\n')
	target.close()
	print 'done'

if __name__ == '__main__':	
	# parseNetEaseHTML()
	# parseYahooHTML()
	parseMsnHTML()
	pass