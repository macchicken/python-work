from math import floor

def is_int(x):
    return x==(floor(x))

print is_int(7.50)

def factorial(x):
    total=x
    x-=1
    while(x>0):
        total*=x
        x-=1
    return total
print factorial(4)

def is_even(x):
    return x%2==0

def is_prime(x):
    result=False
    if x > 1:
        if x==2:
            result=True
        elif not is_even(x):
            temp=x
            x-=1
            while x>=2 :
                if temp%x==0:
                    break
                x-=1
            else:
                result=True
    return result

print is_prime(101)


def reverse(text):
    newstr=""
    length = len(text)
    if length>0:
        for i in range(length):
            newstr+=text[length-(i+1)]
    return newstr
print reverse("ab!@#$%")

def is_vowel(c):
    c=c.lower()
    return c=='a' or c=='e' or c=='i' or c=='o' or c=='u'

def anti_vowel(text):
    newstr=""
    for c in text:
        if not is_vowel(c):
            newstr+=c
    return newstr
print anti_vowel("Hey you!")

score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}
         
def scrabble_score(word):
    total=0
    for c in word:
        if c.isalpha():
            c=c.lower()
            total+=score[c]
    return total
print scrabble_score(" ")


def censor(text,word):
    resultclist =[]
    replacer=len(word)*"*"
    for w in text.split():
        if w.lower()==word:
            resultclist.append(replacer)
        else:
            resultclist.append(w)
    return " ".join(resultclist)

print censor("this hack is wack hack", "hack")


def count(sequence,item):
    totalcount=0
    if type(item) is list:
        for oneitem in item:
            totalcount+=count(sequence,oneitem)
    else:
        for oneelement in sequence:
            if type(oneelement) is str:
                for c in oneelement:
                    if c==item:
                        totalcount+=1
            else:
                if oneelement==item:
                        totalcount+=1
    return totalcount

print count(["a","b","aaawwaatghar","42343"],["a","b"])


#removes all odd numbers in the list
def is_even(number):
    return number%2==0

def purify(numbers):
    newlist=[]
    for number in numbers:
        if type(number) is int:
            if is_even(number):
                newlist.append(number)
    return newlist

print purify([1,2,3,1.00,2.00])


def product(numbers):
    total=1
    for number in numbers:
        if is_int(number):
            total*=number
    return int(total)
print product([4.0,5,5.0])


def remove_duplicates(elements):
    newlist=[]
    for element in elements:
        if element not in newlist:
            newlist.append(element)
    return newlist

print remove_duplicates([1,1,2,2])


#number "/" a float numer can result to an accurate float number,avoid the result normal / operaction between integer to be floor
def is_even(x):
    return x%2==0

def median(numbers):
    templist=numbers
    templist.sort()
    length=len(templist)
    if length>0:
        if is_even(length):
            return (templist[(length/2)-1]+templist[(length/2)])/2.0
        else:
            return templist[(length/2)]
    else:
        return 0

print median([7,12,3,1,6])


#Stocking Out
#an item isn't in stock, then it shouldn't be included in the total. You can't buy or sell what you don't have
groceries = ["banana", "orange", "apple","pear"]

stock = { "banana": 6,
    "apple": 0,
    "orange": 32,
    "pear": 15
}
    
prices = { "banana": 4,
    "apple": 2,
    "orange": 1.5,
    "pear": 3
}

def compute_bill(groceries):
    total=0
    for fruit in groceries:
        if stock[fruit]>0:
            total+=prices[fruit]
            stock[fruit]-=1
    return total

print compute_bill(groceries)