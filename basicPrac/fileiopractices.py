# coding=utf-8
#During the I/O process, data are buffered: 
#this means that they're held in a temporary location before being written to the file. 
#Python doesn't flush the buffer,close() do this
# ("w" stands for "write") stored the result of this operation in a file object, f
# ("r+" stands for "read and write")
# ("r" stands for "read")
from filecmp import dircmp
from os import getcwd
from itertools import permutations
import hashlib

def c(sequence):
	for item in sequence:
		c.items+=1
		yield item

def fileIotest():
	my_list = [i**2 for i in range(1,11)]
	f = open("output.txt", "w")
	for item in my_list:
		f.write(str(item) + "\n")
	f.close()

	#readline():subsequent calls to readline() will return successive lines and append empty line each call
	my_file = open("output.txt", "r")
	print my_file.readline()
	print my_file.readline()
	print my_file.readline()
	my_file.close()

	# Open the file for reading
	read_file = open("output.txt", "r")

	# Use a second file handler to open the file for writing
	write_file = open("output.txt", "w")
	# Write to the file
	write_file.write("Not closing files is VERY BAD.")
	write_file.close()

	# Try to read from the file
	print read_file.read()
	read_file.close()

	#The 'with' and 'as' Keywords
	#file objects contain a special pair of built-in methods: __enter__() and __exit__()
	#'with' and 'as' Keywords invoke thoses exit method to close file
	with open("output.txt", "w") as textfile:
		for item in my_list:
			textfile.write(str(item) + "\n")
	if not textfile.closed:
		print "textfile closing"
		textfile.close()
	print textfile.closed

def compareDirectory(dirc_a,dirc_b,namesToignore):
	comparator=dircmp(dirc_a,dirc_b,ignore=namesToignore)
	for fileName in c(comparator.diff_files):
		print 'different file %s found' % (fileName)
	if comparator.left_only!=[]:print 'only in',dirc_a,comparator.left_only
	if comparator.right_only!=[]:print 'only in',dirc_b,comparator.right_only
	for sub_comparator in comparator.subdirs.values():
		compareDirectory(sub_comparator.left,sub_comparator.right,namesToignore)

def writeGoogleDisFile():
	f = open(getcwd()+"\\1-copy-2.dis", "wb")
	with open(getcwd()+"\\1-copy.dis", "r") as textfile:
		for line in textfile:
			if line.find('=')!=-1:
				temp=line.split('=',1)
				len2=len(temp[1])
				if temp[1][len2-2]==' ':
					f.write(temp[0]+' '+temp[1][:len2-3]+'\n')
				else:f.write(temp[0]+' '+temp[1])
			else:f.write(line)
	if not textfile.closed:
		print 'file closeds'
		textfile.close()
	f.close()

def chineseWordCombinations(guessStr):
	c.items=0
	cmap={}
	for i in range(len(guessStr)):
		cmap['A'+str(i)]=i
	f=open(getcwd()+'\\testchiness.txt', "wb")
	for (A1,B1,C1,D1) in c(permutations(cmap.keys(),4)):
		f.write(guessStr[cmap[A1]]+guessStr[cmap[B1]]+guessStr[cmap[C1]]+guessStr[cmap[D1]]+'\n')
	f.close()
	print 'total of %d permutations' % (c.items)

def hashfile(fileName,blockNum=128):
	with open(fileName,'rb') as target:
		hasher=hashlib.md5()
		blockSize=hasher.block_size
		for chunk in iter(lambda: target.read(blockNum*blockSize), b''):
			hasher.update(chunk)
	return hasher.hexdigest()

def sha1OfFile(filepath):
	with open(filepath, 'rb') as f:
		return hashlib.sha1(f.read()).hexdigest()

def sha512OfFile(filepath):
	with open(filepath, 'rb') as f:
		return hashlib.sha512(f.read()).hexdigest()

def shaOfFile(filepath,flag='hash'):
	if flag=='sha1': return sha1OfFile(filepath)
	elif flag=='sha512': return sha512OfFile(filepath)
	else: return hashfile(filepath)

if __name__ == '__main__':
	# dirc_a='L:\\barry-document'
	# dirc_b='K:\\barry-document'
	# c.items=0
	# compareDirectory(dirc_a,dirc_b,None)
	# print '%d different files found' % (c.items)
	# writeGoogleDisFile()
	# guessStr=['石','银','快','环','宇','联','花','递','新','园','给','流','有','球','浪','闻','宙','河','凰','播','星','人','陨','凤']
	# chineseWordCombinations(guessStr)
	print 'SHA1 checksum: '+shaOfFile('C:\\Users\\chenhui\\Desktop\\mkvtoolnix-unicode-6.5.0-1.7z','sha1')
	print 'sha512 checksum: '+shaOfFile('C:\\Users\\chenhui\\Desktop\\mkvtoolnix-unicode-6.5.0-1.7z','sha512')
	pass