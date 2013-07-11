#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic list exercises

# D. Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent(nums):
  prev_n,new_nums=None,[]
  for number in nums:
	if prev_n!=number:new_nums.append(number)
	prev_n=number
  return new_nums


# E. Given two lists sorted in increasing order, create and return a merged
# list of all the elements in sorted order. You may modify the passed in lists.
# Ideally, the solution should work in "linear" time, making a single
# pass of both lists.
def linear_merge(list1, list2):
  merged_list,i,j=[],0,0
  try:
	while True:
		if list1[i]<=list2[j]:
			merged_list.append(list1[i]);i+=1
		else:
			merged_list.append(list2[j]);j+=1
  except IndexError:None #either list1 or list2 reach the end
  if i==len(list1):merged_list+=list2[j:]
  else: merged_list+=list1[i:]
  return merged_list

def linear_merge_new(list1,list2):
	merged_list,i,j=[],0,0
	len_1,len_2=len(list1),len(list2)
	while i<len_1:
		if list1[i]<=list2[j]:merged_list.append(list1[i]);i+=1
		else:merged_list.append(list2[j]);j+=1
		if j==len_2:
			merged_list+=list1[i:len_1]
			return merged_list
	merged_list+=list2[j:]
	return merged_list

# using generator method next() can lead to a linear time without using index to access and count the length of list,works on any collections
def linear_merge_generator(list1_iter,list2_iter):
	list1_value=next(list1_iter)
	list2_value=next(list2_iter)
	while True:
		if list1_value<=list2_value:
			yield list1_value
			try:
				list1_value=next(list1_iter)
			except StopIteration:
				yield list2_value
				while True:yield next(list2_iter)
		else:
			yield list2_value
			try:
				list2_value=next(list2_iter)
			except StopIteration:
				yield list1_value
				while True:yield next(list1_iter)

def linear_merge_gen(list1,list2):
	merged_iter=linear_merge_generator(iter(list1),iter(list2))
	merged_list=[]
	for element in merged_iter:merged_list.append(element)
	return merged_list

# Note: the solution above is kind of cute, but unforunately list.pop(0)
# is not constant time with the standard python list implementation, so
# the above is not strictly linear time.
# An alternate approach uses pop(-1) to remove the endmost elements
# from each list, building a solution list which is backwards.
# Then use reversed() to put the result back in the correct order. That
# solution works in linear time, but is more ugly.


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


# Calls the above functions with interesting inputs.
def main():
  print 'remove_adjacent'
  test(remove_adjacent([1, 2, 2, 3]), [1, 2, 3])
  test(remove_adjacent([2, 2, 3, 3, 3]), [2, 3])
  test(remove_adjacent([]), [])

  print
  print 'linear_merge'
  test(linear_merge(['aa', 'xx', 'zz'], ['bb', 'cc']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'xx'], ['bb', 'cc', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'aa'], ['aa', 'bb', 'bb']),['aa', 'aa', 'aa', 'bb', 'bb'])
  test(linear_merge(['aa', 'cc'], ['bb', 'dd']),['aa', 'bb', 'cc', 'dd'])
  test(linear_merge(['bb', 'cc', 'xx'],['aa', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])
  
  print
  print 'linear_merge generator version'
  test(linear_merge_gen(['aa', 'xx', 'zz'], ['bb', 'cc']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge_gen(['aa', 'xx'], ['bb', 'cc', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge_gen(['aa', 'aa'], ['aa', 'bb', 'bb']),['aa', 'aa', 'aa', 'bb', 'bb'])
  test(linear_merge_gen(['aa', 'cc'], ['bb', 'dd']),['aa', 'bb', 'cc', 'dd'])
  test(linear_merge_gen(['bb', 'cc', 'xx'],['aa', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])

  print
  print 'new version linear_merge'
  test(linear_merge_new(['aa', 'xx', 'zz'], ['bb', 'cc']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge_new(['aa', 'xx'], ['bb', 'cc', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge_new(['aa', 'aa'], ['aa', 'bb', 'bb']),['aa', 'aa', 'aa', 'bb', 'bb'])
  test(linear_merge_new(['aa', 'cc'], ['bb', 'dd']),['aa', 'bb', 'cc', 'dd'])
  test(linear_merge_new(['bb', 'cc', 'xx'],['aa', 'zz']),['aa', 'bb', 'cc', 'xx', 'zz'])


if __name__ == '__main__':
  main()