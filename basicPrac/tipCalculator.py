"""
A function is a reusable section of code written to perform a specific task in a program. 
You might be wondering why you need to separate your code into functions, 
rather than just writing everything out in one giant block. 
You might have guessed the answer(s) already, but here are some of the big ones:

If something goes wrong in your code, 
it's much easier to find and fix bugs if you've organized your program well.
Assigning specific tasks to separate functions helps with this organization.

By assigning specific tasks to separate functions 
(an idea computer scientists call separation of concerns), 
you make your program less redundant 
and your code more reusable—not only can you repeatedly use the same function in a single program without rewriting it each time, 
but you can even use that function in another program.
When we learn more about objects, 
you'll find out there are a lot of interesting things we can do with functions that belong to those objects (called methods)
"""

def tax(bill):
    """Adds 8% tax to a restaurant bill."""
    bill *= 1.08
    print "With tax: %f" % bill
    return bill

def tip(bill):
    """Adds 15% tip to a restaurant bill."""
    bill *= 1.15
    print "With tip: %f" % bill
    return bill
    
meal_cost = 100
meal_with_tax = tax(meal_cost)
meal_with_tip = tip(meal_with_tax)