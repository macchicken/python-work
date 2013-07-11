#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
from Queue import Queue
from threading import Thread
from urllib2 import urlopen
from urllib2 import HTTPError

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

urlQ=Queue()
lenKey=len('img')

def checkSpecialFilePattern(filePattern,gethttpUrlDict):
	fileList=[os.path.basename(httpUrl) for httpUrl in gethttpUrlDict.keys()]
	return len(fileList)==len(re.findall(filePattern,' '.join(fileList)))

def get_second_word(tuplpe_t):
	return os.path.basename(tuplpe_t[0]).split('-')[2]

def find_number_path(pathname):
	return int(re.search(r'img[\d]+.[\S]*',pathname).group().split('.')[-2][lenKey:])

def read_urls(filename,Screensout=False):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  with open(filename,'rb') as alogfile:
	gethttpUrlDict={}
	specialFile=True
	for line in alogfile:
		if 'puzzle' in line:
			gethttpUrl=re.search(r'GET\s*[\S]+puzzle[\S]+\s*HTTP',line)
			if gethttpUrl!=None:
				gethttpUrl=gethttpUrl.group().split()[1]
				if gethttpUrl in gethttpUrlDict:gethttpUrlDict[gethttpUrl]+=1
				else:
					gethttpUrlDict[gethttpUrl]=1
					specialFile=(specialFile and re.search(r'[\S]+-[\S]+-[\S]+',os.path.basename(gethttpUrl))!=None)
  if Screensout:
	print gethttpUrlDict;print 'duplicate urls:'
	print '\n'.join([httpUrl for httpUrl,count in gethttpUrlDict.items() if count>1])
  keyfn=None
  if specialFile:keyfn=get_second_word
  httpDomainName='http://'+filename.split('_',1)[1]
  return [httpDomainName+gethttpUrl for gethttpUrl,_ in sorted(gethttpUrlDict.items(),key=keyfn)]

def report_hook(blocksCounts,blockSize,fileSize):
	print 'number of blocks been transferred',blocksCounts
	print 'one block size is',blockSize,'bytes'
	print 'total size of the file',fileSize

def createLocalimgHtml(filename,downloadedFileList,sortkey=None):
	with open(filename,'wb') as localHtml:
		localHtml.write('<verbatim>\n<html>\n<body>\n')
		if sortkey:downloadedFileList=sorted(downloadedFileList,key=sortkey)
		for onefile in downloadedFileList:
			localHtml.write('<img src="'+onefile+'">')
		localHtml.write('\n</body>\n</html>')

def downloadFilebyUrl(requestUrl,FileName):
	print 'downloading '+requestUrl+' '+FileName
	try:
		conn = urlopen(requestUrl);target = open(FileName, "wb")
		target.write(conn.read())
		conn.close();target.close()
	except HTTPError:
		print 'HTTPError on',requestUrl

def downloadFileWorker(downloadedFileList,dest_dir):
	while True:
		img_url,imgFilename=urlQ.get(block=True)
		downloadFilebyUrl(img_url,dest_dir+os.sep+imgFilename)
		downloadedFileList.append(imgFilename)
		urlQ.task_done()

def download_images(img_urls, dest_dir, mutilTask=1):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.access(dest_dir,os.F_OK):os.makedirs(dest_dir)
  file_index,downloadedFileList=0,[]
  for img_url in img_urls:
	try:
		imgFilename='img'+str(file_index)+'.jpg';file_index+=1
		if mutilTask>1:urlQ.put((img_url,imgFilename));
		else:
			print 'downloading',img_url
			urllib.urlretrieve(img_url,dest_dir+os.sep+imgFilename,reporthook=report_hook)
			downloadedFileList.append(imgFilename)
	except ContentTooShortError:print 'try later',img_url
	except IOError as IOE:print IOE
  if mutilTask>1:
	for i in range(mutilTask):
		t=Thread(target=downloadFileWorker,args=(downloadedFileList,dest_dir))
		t.daemon=True;t.start()
	urlQ.join()
	sortkey=find_number_path
  if downloadedFileList!=[]:createLocalimgHtml(dest_dir+os.sep+'index.html',downloadedFileList,sortkey)

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir,10)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
  # print '\n'.join(read_urls('animal_code.google.com'))