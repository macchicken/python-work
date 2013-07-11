num = 1

while num<=10:# Fill in the condition (before the colon)
    print num**2
    


"""
the break is a one-line statement that means "exit the current loop." 
An alternate way to make our counting loop exit and stop executing is with the break statement
"""
count = 0

while True:
    print count
    count += 1
    if count >= 10:
        break
    else:
        count-=0.5
"""
While / else
while/else is similar to if/else, but there is a difference: 
the else block will execute anytime the loop condition is evaluated to False. 
This means that it will execute if the loop is never entered or if the loop exits normally. 
If the loop exits as the result of a break, the else will not be executed.
"""

import random

print "Lucky Numbers! 3 numbers will be generated."
print "If one of them is a '5', you lose!"

count = 0
while count < 3:
    num = random.randint(1, 6)
    print num
    count += 1
    if num == 5:
        print "Sorry, you lose!"
        break
else:
    print "You win!"


"""
current code generates a random number in the range 1 - 9 (remember, the upper bound is exclusive).
Allow the user to guess what the number is three times.
"""
from random import randrange

random_number = randrange(1, 10)

count = 0
# Start your game!
while count<3:
    guess = int(raw_input("Enter a guess:"))
    count+=1
    if guess==random_number:
        print 'You win!'
        break
else:
    print 'You lose.'


"""
String manipulation is useful in for loops if you want to modify some content in a string. 
A for loop makes it possible to examine each character, one a time.
"""
s = "A bird in the hand..."

length = len(s)
for c in range(length):
    if c<length-1:
        if s[c]=='a' or s[c]=='A':
            print 'X',
        else:
            print s[c],
    else:
        print s[c]




"""
loop over a dictionary
"""
d = {'x': 9, 'y': 10, 'z': 20}

for key in d:
    print str(key)," ",d[key]



"""
enumerate works by supplying a corresponding index to each element in the list that you pass it. 
Each time you go through the loop, index will be one greater, 
and item will be the next item in the sequence.
"""
choices = ['pizza', 'pasta', 'salad', 'nachos']

print 'Your choices are:'
for index, item in enumerate(choices):
    print index+1, item


"""
zip will create pairs of elements when passed two lists, and will stop at the end of the shorter list
zip can handle three or more lists as well
"""
list_a = [3, 9, 17, 15, 19]
list_b = [2, 4, 8, 10, 30, 40, 50, 60, 70, 80, 90]

for a, b in zip(list_a, list_b):
    if a>=b:
        print a,
    else:
        print b


"""
for/else loop
the else statement is executed after the for, but only if the for ends normally—that is, not with a break
"""
fruits = ['banana', 'apple', 'orange', 'tomato', 'pear', 'grape']

print 'You have...'
for f in fruits:
    if f == 'biscuit':
        print 'A biscuit is not a fruit!'
        break
    print 'A', f
else:
    print 'A fine selection of fruits!'


fruits = ['banana', 'apple', 'orange', 'tomato', 'pear', 'grape']

choice = raw_input('You want...')
for f in fruits:
    if f == choice:
        print 'A %s is a fruit!' % choice
        print 'A fine selection of fruits!'
        break
else:
    print 'A %s is not a fruit!' % choice