#!/usr/bin/python -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

"""A tiny Python program to check that Python is working.
Try running this program from the command line like this:
  python hello.py
  python hello.py Alice
That should print:
  Hello World -or- Hello Alice
Try changing the 'Hello' to 'Howdy' and run again.
Once you have that working, you're ready for class -- you can edit
and run Python code; now you just need to learn Python!
"""

import sys
from datetime import date
from datetime import timedelta

# Define a main() function that prints a little greeting.
def main():
  # Get the name from the command line, using 'World' as a fallback.
  if len(sys.argv) >= 2:
    name = sys.argv[1]
  else:
    name = 'World'
  print 'Hello', name

def calWorkingDates(beginDay=date.today()):
	today=date.today()
	workingDates=0
	while(beginDay<=today):
		weekday=beginDay.isoweekday()
		if (weekday!=6 and weekday!=7):#is not wed and sunday
			workingDates+=1
		beginDay+=timedelta(days=1)
	return "workingDates",workingDates

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
  print calWorkingDates(date(2014,9,16))
