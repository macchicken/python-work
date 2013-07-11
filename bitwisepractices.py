"""
Bitwise operations are operations that directly manipulate bits. 
In all computers, numbers are represented with bits, a series of zeros and ones
can only do bitwise operations on an integer
Trying to do them on strings or floats will result in nonsensical output
"""

print 5 >> 4  # Right Shift
print 5 << 1  # Left Shift
print 8 & 5   # Bitwise AND
print 9 | 4   # Bitwise OR
print 12 ^ 42 # Bitwise XOR
print ~88     # Bitwise NOT

#The Base 2 Number System,Python write numbers in binary format by starting the number with 0b
print 0b1,    #1
print 0b10,   #2
print 0b11,   #3
print 0b100,  #4
print 0b101,  #5
print 0b110,  #6
print 0b111   #7
print "******"
print 0b1 + 0b11
print 0b11 * 0b11

#bin function takes an integer as input and returns the binary representation of that integer in a string
print bin(1)
print bin(2)
print bin(3)
print bin(4)
print bin(5)


#the second parameter of int function
#given a string containing a number and the base that number is in, 
#the function will return the value of that number in base ten
print int("1",2)
print int("10",2)
print int("111",2)
print int("0b100",2)
print int(bin(5),2)
print int("0b11001001",2)


#left and right shift bitwise operators
shift_right = 0b1100
shift_left = 0b1

shift_right = shift_right>>2
shift_left = shift_left<<2

print bin(shift_right)
print bin(shift_left)



#AND (&) operator compares two numbers on a bit level and 
#returns a number where the bits of that number are turned on if the corresponding bits of both numbers are 1
print bin(0b1110 & 0b101)




#OR (|) operator compares two numbers on a bit level and 
#returns a number where the bits of that number are turned on if either of the corresponding bits of either number are 1
print bin(0b1110|0b101)

#XOR (^) or exclusive or operator compares two numbers on a bit level and 
#returns a number where the bits of that number are turned on if either of the corresponding bits of the two numbers are 1 but not both
print bin(0b1110 ^ 0b101)



#NOT operator (~) just flips all of the bits in a single number
print ~1
print ~2
print ~3
print ~42
print ~123



#A bit mask is basically just a variable that aids you with bitwise operations

#takes an integer as input and checks to see if the fourth bit from the right is on.
def check_bit4(x):
    mask=0b1000
    if x&mask>0:
        return "on"
    else:
        return "off"
print check_bit4(16)

#se masks to turn a bit in a number on using |
a = 0b10111011
mask= 0b100
print bin(a|mask)

#XOR (^) operator is very useful for flipping bits. 
#Using ^ on a bit with the number one will return a result where that bit is flipped
a = 0b11101110
mask = 0b11111111
print bin(a^mask)

#also use the left shift (<<) and right shift (>>) operators to slide masks into place.
#on the nth bit from the right of an integer
#returns the number with the nth bit flipped
def flip_bit(number,n):
    mask = (0b1<<(n-1))
    return bin(number^mask)
print flip_bit(5,9)