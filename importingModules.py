"""
Generic Imports
There is a Python module named math that includes a number of useful variables and functions, 
and (as you've probably guessed) sqrt() is one of those functions. 
In order to get to it, all you need is the import keyword. 
When you simply import a module this way, it's called a generic import.

import math

print math.sqrt(25)
"""

"""
Function Imports
Importing the entire math module is kind of annoying for two reasons, 
though: first, we really only want the sqrt function, and second, 
we have to remember to type math.sqrt() any time we want to retrieve that function from the math module.

Thankfully, it's possible to import only certain variables or functions from a given module. 
Pulling in just a single function from a module is called a function import, 
and it's done using the from keyword from module import function

from math import sqrt

print sqrt(25)
"""

"""
Universal Imports
What if we want a large selection (or all) of the variables and functions available in a module? 
We can import module, but there's another option.

When you import math, you're basically saying: 
"Bring the Math Box to my apartment so I can use all the cool stuff in it." 
Whenever you want a tool in math, you have to go to the box and pull out the thing you want 
(which is why you have to type math.name for everything—even though the box is in your apartment, 
all the cool stuff you want is still in that box).

When you choose from math import sqrt, you're saying: 
"Bring me only the square root tool from the Math Box, 
and don't bring the Math Box to my apartment." 
This means you can use sqrt without reference to math, 
but if you want anything else from math, you have to import it separately, 
since the whole Math Box isn't in your apartment for you to dig through.

The third option is to say: 
"Don't bring the Math Box to my apartment, but bring me absolutely every tool in it." 
This gives you the advantage of having a wide variety of tools, 
and since you have them in your apartment and they're not all still stuck in the Math Box, 
you don't have to constantly type math.name to get what you want.
The syntax for this is: from module import *

from math import *
print sqrt(25)
"""

"""
Here Be Dragons
Here's something we've learned in life (and not just from programming): 
just because you can do something doesn't mean that you should.

Universal imports may look great on the surface, but they're not a good idea for one very important reason: 
they can fill your program with a ton of variable and function names, 
but without the safety of those names still being associated with the module(s) they came from.

If you have a function of your very own named sqrt and you import math, 
your function is safe: there is your sqrt and there is math.sqrt, and ne'er the twain shall meet. 
If you do from math import *, however, you have a problem: namely, 
two different functions with the exact same name.

Even if your own definitions don't directly conflict with names from imported modules, 
if you import * from several modules at once, 
there won't be any way for you to figure out which variable or function came from where. 
It'd be like having someone dump a ton of random stuff from a bunch of different boxes in your apartment, 
then throwing the boxes away so you can't even see where the stuff came from.

For these reasons, it's best to stick with either import module and suffer the inconvenience of having to type module.name, 
or just import specific variables and functions from various modules as needed.
"""

import math            # Imports the math module
everything = dir(math) # Sets everything to a list of things from math
print everything       # Prints 'em all!