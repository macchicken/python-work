#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
# import commands
import subprocess

"""Copy Special exercise
"""

class DuplicateNameError(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)


def c(sequence):
	for s in sequence:
		c.items+=1
		yield s

# Write functions and modify main() to call them
# returns a list of the absolute paths of the special files in the given directory
# assumption:names are not repeated across the directories
# check the assumption and error out if it's violated
def get_special_paths(dir):
	special_paths,absolutepath=[],os.path.abspath(dir)
	for fileName in os.listdir(dir):
		if re.search(r'__[\w]+__',fileName):
			special_paths.append(absolutepath+os.sep+fileName)
	return special_paths

def checkDuplicateBasename(filePathList):
	basenameDict={}
	for onefile in filePathList:
		if os.path.isfile(onefile):filebasename=os.path.basename(onefile)
		else:filebasename=os.path.split(onefile)[1]
		if filebasename not in basenameDict:basenameDict[filebasename]=onefile
		else:raise DuplicateNameError('duplicate file found '+onefile+' '+basenameDict[filebasename])

# given a list of paths, copies those files and directories into the given directory	
def copy_to(paths, dir):
	if not os.access(dir,os.F_OK):os.makedirs(dir)
	special_paths=[]
	for path in paths:
		if os.path.isfile(path):special_paths.append(path)
		else:special_paths+=get_special_paths(path)
	checkDuplicateBasename(special_paths)
	c.items=0
	for onefile in c(special_paths):
		try:
			if os.path.isdir(onefile):shutil.copytree(onefile,dir+os.sep+os.path.basename(onefile))
			else:shutil.copy(onefile,dir)
		except IOError as IOE:print IOE;c.items-=1;continue
		except WindowsError as WE:print WE;c.items-=1;continue
	return 'total %d files are successfully copied' % (c.items)

# given a list of paths, zip those files up into the given zipfile,7z is able to zip by using relative path
def zip_to(paths, zippath,verbose=False):
	#filter out the unavailable path,if get down to empty list,return
	availablePath=[path for path in paths if os.access(path,os.F_OK)]
	if availablePath==[]:print 'no available path for zipping';return
	# availablePath=paths
	availableFiles=[]
	#no matter whether a file is special or not
	for apath in availablePath:
		if os.path.isfile(apath):availableFiles.append(apath)
		else:availableFiles+=get_special_paths(apath)
	checkDuplicateBasename(availableFiles)
	commandCall=["7z","a",zippath]+availableFiles
	if verbose:
		print 'available path to zip'
		for apath in availablePath:print apath
		print 'Command I am going to do:',
		for parameter in commandCall:print parameter,
	returnCode=subprocess.call(commandCall)
	if returnCode!=0:sys.exit(returnCode)

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # Call your functions
  if sys.platform.index('win')==0:
	dircs=[]
	for arg in args:
		if arg=='.':dircs.append(os.getcwd())
		else:dircs.append(arg)
  else:dircs=args
  try:
	if todir!='' and tozip=='':print copy_to(dircs,todir)
	elif todir=='' and tozip!='':zip_to(dircs,tozip)
	else:
		for dirc in dircs:print '\n'+'\n'.join(get_special_paths(dirc))
  except DuplicateNameError as E:print E


if __name__ == "__main__":
  main()
  # print get_special_paths(os.getcwd())
  # print get_special_paths('special-copy-1')
  # testPath=['copyspecial','K:\\barry-document\\hc105','K:\\barry-document\\hc105\\python\\copyspecial','K:\\barry-document\\hc105\\python\\copyspecial\\zz__something.jpg','copyspecial.py']
  # checkDuplicateBasename(testPath)
  # print copy_to(testPath,'special-copy')
  # zip_to(testPath,'test.zip',verbose=True)