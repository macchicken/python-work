#Sequence Types - str, unicode, list, tuple, bytearray, buffer, xrange
"""
A list index behaves like any other variable name! It can be used to access as well as assign values
"""

zoo_animals = ["pangolin", "cassowary", "sloth", "tiger"]
# Last night our zoo's sloth brutally attacked the poor tiger and ate it whole.

# The ferocious sloth has been replaced by a friendly hyena.
zoo_animals[2] = "hyena"

# What shall fill the void left by our dear departed tiger?
# Your code here!
zoo_animals[3] = "penguin"
print zoo_animals


"""
A list doesn't have to have a fixed length you can add items to the end of a list any time you like!
In Python, we say lists are mutable: that is, they can be changed.
You can add items to lists with the built-in list function append()
You can get the number of items in a list with the len() function
"""
suitcase = [] 
suitcase.append("sunglasses")

# Your code here!
suitcase.append("bathing suit")
suitcase.append("slipper")
suitcase.append("camera")

# Set this to the length of suitcase
list_length = len(suitcase)

print "There are %d items in the suitcase." % list_length
print suitcase

suitcase = ["sunglasses", "hat", "passport", "laptop", "suit", "shoes"]


"""
List Slicing
If you only want a small part of a list, that portion can be accessed using a special notation in the index brackets. 
list_name[a:b] will return a portion of list_name starting with the index a and ending before the index b
"""
# The first two items
first = suitcase[0:2] 
# Third and fourth items
middle = suitcase[2:4]  
# The last two items
last = suitcase[len(suitcase)-2:len(suitcase)]
print "first "
print first
print "middle "
print middle
print "last "
print last


"""
Slicing Lists and Strings
You can slice a string exactly like a list! 
In fact, you can think of strings as lists of characters: each character is a sequential item in the list, 
starting from index 0.
If your list slice includes the very first or last item in a list (or a string), 
the index for that item doesn't have to be included. 
"""
animals = "catdogfrog"
# The first three characters of animals
cat = animals[:3]   
# The fourth through sixth characters
dog = animals[3:6]   
# From the seventh character to the end
frog = animals[6:]


"""
Maintaining Order
You can search through a list with the index() function. my_list.index("dog") will return the first index that contains the string "dog". 
An error will occur if there is no such item
Items can be added to the middle of a list (instead of to the end) with the insert() function. 
my_list.insert(4,"cat") adds the item "cat" at index 4 of my_list, 
and moves the item previously at index 4 and all items following it to the next index (that is, they all get bumped forward by one).
"""
animals = ["aardvark", "badger", "duck", "emu", "fennec fox"]
# Use index() to find "duck"
duck_index = animals.index("duck")
animals.insert(duck_index,"cobra")
print animals # Observe what prints after the insert operation


"""
For One and All
A variable name follows the for keyword; it will be assigned the value of each list item in turn. 
in list_name designates list_name as the list the loop will work on. 
The line ends with a colon (:) and the indented code that follows it will be executed once per item in the list.
for variable in list_name:
	Do stuff!

If your list is a jumbled mess, you may need to sort() it. 
Operation: my_list.sort([cmp[, key[, reverse]]])
my_list.sort() will sort the items in my_list in increasing numerical/alphabetical order.
In general, the key and reverse conversion processes are much faster than specifying an equivalent cmp function.
It's worth noting that sort() does not return a new list;
instead, your existing my_list is sorted in place (the sorted version replaces the unsorted version)
sorted(my_list) is able to sort a list from lowest to highest,
however reversed(my_list) just reverses a list order but not from highest to lowest and return a listreverseiterator object.
both sorted and reversed have side effect.
"""
my_list = [1,9,3,8,5,7]

for number in my_list:
    # Your code here
    print 2*number

start_list = [5, 3, 1, 2, 4]
square_list = []

# Your code here!
start_list.sort()
for number in start_list:
    square_list.append(number**2)

print square_list

"""
A dictionary is similar to a list, but you access values by looking up a key instead of an index. 
A key can be any string or number. Dictionaries are enclosed in curly braces
Dictionaries are great for things like phone books (pairing a name with a phone number), 
login pages (pairing an e-mail address with a username), and more!
A new key-value pair in a dictionary is created by assigning a new key
An empty pair of curly braces {} is an empty dictionary, just like an empty pair of [] is an empty list
The length len() of a dictionary is the number of key-value pairs it has. 
Each pair counts only once, even if the value is a list. 
(That's right: you can put lists inside dictionaries!)
Items can be removed from a dictionary with the del command
del(my_list[index]) is like .pop in that it will remove the item at the given index, but it won't return it
my_list.remove(value) will remove the the first item from my_list that has a value equal to value. 
The difference between del and .remove() is:
del deletes a key and its value based on the key you tell it to delete.
.remove() removes a key and its value based on the value you tell it to delete
.pop(index) will remove the item at index from the list and return it to you
"""
# Assigning a dictionary with three key-value pairs to residents:
residents = {'Puffin' : 104, 'Sloth' : 105, 'Burmese Python' : 106}
print residents['Puffin'] # Prints Puffin's room number
print residents['Sloth']
print residents['Burmese Python']


menu = {} # Empty dictionary
menu['Chicken Alfredo'] = 14.50 # Adding new key-value pair
print menu['Chicken Alfredo']

# Your code here: Add some dish-price pairs to menu!
menu['Spam'] = 2.50
menu['Fire rice'] = 2.00
menu['Fish and chips'] = 8.50
menu['Chicken tikka masala'] = 8.00
menu['kebab'] = 9.00

print "There are " + str(len(menu)) + " items on the menu."
print menu


# key - animal_name : value - location 
zoo_animals = { 'Unicorn' : 'Cotton Candy House',
'Sloth' : 'Rainforest Exhibit',
'Bengal Tiger' : 'Jungle House',
'Atlantic Puffin' : 'Arctic Exhibit',
'Rockhopper Penguin' : 'Arctic Exhibit'}
# A dictionary (or list) declaration may break across multiple lines

# Removing the 'Unicorn' entry. (Unicorns are incredibly expensive.)
del zoo_animals['Unicorn']

# Your code here!
del zoo_animals['Sloth']
del zoo_animals['Bengal Tiger']
zoo_animals['Rockhopper Penguin'] = 'ahhahahah'

print zoo_animals


inventory = {'gold' : 500,
'pouch' : ['flint', 'twine', 'gemstone'], # Assigned a new list to 'pouch' key
'backpack' : ['xylophone','dagger', 'bedroll','bread loaf']}

# Adding a key 'burlap bag' and assigning a list to it
inventory['burlap bag'] = ['apple', 'small ruby', 'three-toed sloth']

# Sorting the list found under the key 'pouch'
inventory['pouch'].sort() 
# Here the dictionary access expression takes the place of a list name 


inventory['pocket']=['seashell','strange berry','lint']
backpacklist = inventory['backpack']
backpacklist.remove('dagger')
backpacklist.sort()
inventory['backpack']=backpacklist
gold = inventory['gold']
inventory['gold'] = gold+50
print inventory


#Print out all the data in your students list
lloyd = {
    "name": "Lloyd",
    "homework": [ 90, 97, 75, 92],
    "quizzes": [88, 40, 94],
    "tests": [75, 90]
}
alice = {
    "name": "Alice",
    "homework": [100,92,98,100],
    "quizzes": [82,83,91],
    "tests": [89,97]
}
tyler = {
    "name": "Tyler",
    "homework": [0,87,75,22],
    "quizzes": [0,75,78],
    "tests": [100,100]
}

students=[lloyd,alice,tyler]
for student in students:
    for data in student.values():
        print data


lloyd = {
    "name": "Lloyd",
    "homework": [90, 97, 75, 92],
    "quizzes": [88, 40, 94],
    "tests": [75, 90]
}
alice = {
    "name": "Alice",
    "homework": [100, 92, 98, 100],
    "quizzes": [82, 83, 91],
    "tests": [89, 97]
}
tyler = {
    "name": "Tyler",
    "homework": [0, 87, 75, 22],
    "quizzes": [0, 75, 78],
    "tests": [100, 100]
}

students=[lloyd,alice,tyler]
homeworkbase=0.1
quizzesbase=0.3
testbase=0.6

#weighted average of a class
def average(scores):
    total=0
    for score in scores:
        total+=score
    return total/len(scores)

def get_average(student):
    homeworkscores=student["homework"]
    quizzescores=student["quizzes"]
    testscores=student["tests"]
    return average(homeworkscores)*homeworkbase+average(quizzescores)*quizzesbase+average(testscores)*testbase
    
def get_letter_grade(score):
    cal_score = round(score)
    if cal_score>=90:
        return "A"
    elif 80<=cal_score<90:
        return "B"
    elif 70<=cal_score<80:
        return "C"
    elif 60<=cal_score<70:
        return "D"
    else:
        return "F"

def get_class_average(students):
    scores=[]
    for student in students:
        scores.append(get_average(student))
    return average(scores)
    
numericalgrade = get_class_average(students)
print numericalgrade
print get_letter_grade(numericalgrade)



"""
The Python range() function is just a shortcut for generating a list, 
so you can use ranges in all the same places you can use lists.
A range can take 1, 2 or 3 arguments. If you use one argument, 
it starts the range at zero and increments by 1 until the size reaches 1 less than the range
If you use two arguments, the first argument is the start for the range and the second argument is the same as above
If you use 3 arguments, the range's first argument is the number the list starts at, 
the second number is where the list ends, 
and the third argument is how much you should increment by instead of the default increment of 1
"""
def my_function(x):
    for i in range(0, len(x)):
        x[i] = x[i] * 2
    return x

print my_function([0,1,2])

m = [1, 2, 3]
n = [4, 5, 6]
o = [7, 8, 9]

#Using an arbitrary number of lists is no different than using an arbitrary number of any other object in a function
def join_lists(*lists):
    finallist = lists[0]
    for i in range(1,len(lists)):
        for j in range(0,len(lists[i])):
            finallist.append(lists[i][j])
    return finallist

print join_lists(m, n, o)


#takes a single list and concatenates all the sublists that are part of it into a single list
n = [[1, 2, 3], [4, 5, 6, 7, 8, 9]]

def flatten(x):
    finallist = x[0]
    for i in range(1,len(x)):
        if type(x[i]) is list:
            for j in range(0,len(x[i])):
                finallist.append(x[i][j])
        else:
            finallist.append(x[i])
    return finallist

print flatten(n)

# list comprehension
#List comprehensions provide a concise, intuitive way to generate lists using the 'for in' and 'if' keywords
cubes_by_four = [x**3 for x in range(1,11) if (x**3)%4==0]
print cubes_by_four


"""
List Slicing Syntax [start:end:stride]
Where start describes where the slice starts (inclusive), 
end is where it ends (exclusive), and stride describes the space between items in the sliced list
if you don't pass a particular index to the list slice, 
Python will pick a default. 
The default for the starting index is the first element of the list; 
the default for the ending index is the final element of the list; 
and the default for the stride index is 1
A positive stride progresses through the list from left to right; 
a negative stride progresses through the list from right to left
"""

l = [i ** 2 for i in range(1, 11)]
# Should be [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
print l[2:9:2]

my_list = range(1, 11)

backwards = my_list[::-1]
print backwards
garbled = "!XeXgXaXsXsXeXmX XtXeXrXcXeXsX XeXhXtX XmXaX XI"
message = garbled[::-2]
print message

to_21 = range(1,22)
odds =  to_21[::2]
middle_third = to_21[7:14:1]
print odds
print middle_third

if __name__ == '__main__':
	ta_data=[('Peter','USA','CS262'),('Andy','USA','CS212'),('Sarah','England','CS101'),
			 ('Gundega','Latvia','CS373'),('Job','USA','CS387'),('Sean','USA','CS253')]
	ta_facts=[name+' lives in '+country+' and is TA for '+course for name,country,course in ta_data if country!='USA']
	ta_300=[name+' is the TA for '+course for name,country,course in ta_data if 'CS3' in course]