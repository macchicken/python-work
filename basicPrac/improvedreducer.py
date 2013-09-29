#!/usr/bin/env python
# A more advanced Reducer, using Python iterators and generators.
# operation of itertools.groupby(iterable[, key]) is similar to the uniq filter in Unix
# It generates a break or new group every time the value of the key
# function changes (which is why it is usually necessary to have sorted the data using the same key function)

from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_input(file,separator='\t'):
	for line in file:
		yield line.rstrip().split(separator,1)

def main(separator='\t'):
	# input comes from STDIN (standard input)
	# data=read_mapper_input(sys.stdin,separator=separator)
	data=[['a',1],['a',1],['a',1],['b',1],['b',1]]
	# groupby groups multiple word-count pairs by word,
	# and creates an iterator that returns consecutive keys and their group:
	#   current_word - string containing a word (the key)
	#   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
	for current_word,group in groupby(data,itemgetter(0)):
		try:
			total_count=sum(int(count) for current_word,count in group)
			print "%s%s%d" % (current_word,separator,total_count)
		except ValueError:
			# count was not a number, so silently discard this item
			pass

if __name__=="__main__":
	main()