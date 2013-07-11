"""
function can be defined as mulit arguments with *args
"""

from math import sqrt
from math import pi

city_prices = {'Charlotte': 183, 'Tampa': 220, 'Pittsburgh': 222, 'Los Angeles': 475}
singleday = 40

def shut_down(s):
    arg = s.lower()
    if arg=="yes":
        return "Shutting down..."
    elif arg=="no":
        return "Shutdown aborted!"
    else:
        return "Sorry, I didn\'t understand you."

def distance_from_zero(distance):
    input_type = type(distance)
    if input_type is int or input_type is float:
        return abs(distance)
    else:
        return "Not an integer or float!"


def area_of_circle(radius):
    input_type = type(radius)
    if input_type is int or input_type is float:
        return pi*(radius**2)
    else:
        return "not a valid input!"

def hotel_cost(nights):
    if type(nights) is int:
        return nights*140
    else:
        return "Error"

def plane_ride_cost(city):
    if type(city) is unicode:
        return city_prices.get(city,0)
    else:
        return "Error"

def rental_car_cost(days):
    if type(days) is int:
        total = days*singleday
        if days>=7:
            return total-50
        elif days>=3:
            return total-20
        else:
            return total
    else:
        return "Error"

def trip_cost(city,days,spending_money):
    ridercost = plane_ride_cost(city)
    if ridercost=="Error":
        return "not a valid input for city"
    else:
        hotelcost=hotel_cost(days)
        if hotelcost=="Error":
            return "not a valid input for days"
        else:
            return rental_car_cost(days)+ridercost+hotelcost+spending_money

def hotel_cost(nights):
    return nights * 140

def add_monthly_interest(balance):
    return balance * (1 + (0.15 / 12))

def make_payment(payment, balance):
	new_balance = balance-payment
	new_balance = add_monthly_interest(new_balance)
        return "You still owe: " + str(new_balance)

print trip_cost("Los Angeles",5,600)
bill = hotel_cost(5)
print make_payment(100,bill)

print area_of_circle(5.0)

print shut_down("Nop")

print sqrt(13689)

print distance_from_zero(-10.0)

#Arbitrary number of arguments
m = 5
n = 13
def add_function(*args):
    total = 0
    for number in args:
        total+=number
    return total

print add_function(m,n)


"""
Anonymous Functions
Only we don't need to actually give the function a name; 
it does its work and returns a value without one. 
That's why the function the lambda creates is an anonymous function
pass the lambda to filter, filter uses the lambda to determine what to filter, 
and the second argument is the list it does the filtering on
"""
squares=[x**2 for x in range(1,11)]
print filter(lambda x:(x>30 and x<70),squares)

garbled = "IXXX aXXmX aXXXnXoXXXXXtXhXeXXXXrX sXXXXeXcXXXrXeXt mXXeXsXXXsXaXXXXXXgXeX!XX"
message = filter(lambda c:(c!='X' and c!='x'),garbled)
print message

f = lambda Y,M,E,U,O:(1*U+10*O+100*Y)==(1*E+10*M)**2
print f(1,2,3,4,5)