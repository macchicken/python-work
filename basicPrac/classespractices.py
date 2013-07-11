"""
A basic class consists only of the class keyword, the name of the class, 
and the class from which the new class inherits in parentheses
"""
#__init__() is required for classes, and it's used to initialize the objects it creates
#always takes at least one argument, self, that refers to the object being created
#__init__() as the function that "boots up" each object the class creates
#the first parameter that __init__() receives to refer to the object being created(the instance object)
#this parameter gives the object being created its identity
#the scope of a variable is the context in which it's visible to the program
#dealing with classes, you can have variables that are available everywhere (global variables), 
#variables that are only available to members of a certain class (member variables), 
#and variables that are only available to particular instances of a class (instance variables)

class Animal(object):
    is_alive = True
    def __init__(self, name, age):
        self.name = name
        self.age = age

zebra = Animal("Jeffrey", 2)
giraffe = Animal("Bruce", 1)
panda = Animal("Chad", 7)

print zebra.name, zebra.age, zebra.is_alive
print giraffe.name, giraffe.age, giraffe.is_alive
print panda.name, panda.age, panda.is_alive


#Inheritance is the process by which one class takes on the attributes and methods of another, 
#and it's used to express an is-a relationship,Inheritor don't need to defind its own init method despite u want a differnt one...
#also can class base class init method
class Customer(object):
    """Produces objects that represent customers."""
    def __init__(self, customer_id):
        self.customer_id = customer_id
        
    def display_cart(self):
        print "I'm a string that stands in for the contents of your shopping cart!"

class ReturningCustomer(Customer):
    #def __init__(self, customer_id):
     #   self.customer_id = customer_id
        
    def display_order_history(self):
        print "I'm a string that stands in for your order history!"

monty_python = ReturningCustomer("ID: 12345")
monty_python.display_cart()
monty_python.display_order_history()


class ShoppingCart(object):
	"""Creates shopping cart objects
	for users of our fine website."""
	items_in_cart = {}
	def __init__(self, customer_name):
		self.customer_name = customer_name
		
	def add_item(self, product, price):
		"""Add product to the cart."""
		
		if not product in self.items_in_cart:
			self.items_in_cart[product] = price
			print product + " added."
		else:
			print product + " is already in the cart."
		
	def remove_item(self, product):
		"""Remove product from the cart."""
		
		if product in self.items_in_cart:
			del self.items_in_cart[product]
			print product + " removed."
		else:
			print product + " is not in the cart."

my_cart = ShoppingCart("Barry")
my_cart.add_item("apple",1)
my_cart.add_item("vegetable",5)
my_cart.add_item("apple",2)

#override and access the attributes or methods of a superclass with built-in super call
#The syntax,method() is a method from the base class:
#class DerivedClass(Base):
#   def some_method(self):
#       super(DerivedClass, self).method()

class Employee(object):
	"""Models real-life employees!"""
	def __init__(self, employee_name):
		self.employee_name = employee_name
	
	def calculate_wage(self, hours):
		self.hours = hours
		return hours * 20.00

class PartTimeEmployee(Employee):
    def calculate_wage(self,hours):
        self.hours=hours
        return hours*12.00
    def full_time_wage(self,hours):
        return super(PartTimeEmployee,self).calculate_wage(hours)

barry = PartTimeEmployee("Barry")
print barry.calculate_wage(1)
milton = PartTimeEmployee("Milton")
print milton.full_time_wage(10)

#simple classes practice example
class Triangle(object):
    number_of_sides = 3
    def __init__(self,angle1,angle2,angle3):
        self.angle1=angle1
        self.angle2=angle2
        self.angle3=angle3
    def check_angles(self):
        return (self.angle1+self.angle2+self.angle3)==180

class Equilateral(Triangle):
    angle = 60
    def __init__(self):
        super(Equilateral,self).__init__(self.angle,self.angle,self.angle)

my_triangle = Triangle(90,45,45)
print my_triangle.number_of_sides
print test.check_angles()
equilatriangle = Equilateral()
print equilatriangle.check_angles()
print equilatriangle.angle1
print equilatriangle.angle3
print equilatriangle.angle2


#other simple classes practice example
class Car(object):
    condition = "new"
    def __init__(self, model, color, mpg):
        self.model = model
        self.color = color
        self.mpg = mpg
    def displayCar(self):
        print "This is a %s %s with %s MPG." % (self.color,self.model,str(self.mpg))
    def driveCar(self):
        self.condition="used"

class ElectricCar(Car):
    def __init__(self,model,color,mpg,typeOfBattery):
        super(ElectricCar,self).__init__(model,color,mpg)
        self.typeOfBattery=typeOfBattery
    def driveCar(self):
        self.condition="like new"

myCar = ElectricCar("DeLorean", "silver", 88,"molten salt")
print myCar.typeOfBattery
print myCar.displayCar()
print myCar.condition
myCar.driveCar()
print myCar.condition
print myCar.__repr__()

#__repr__() method providing a return value ell Python how to represent an object of our class
#by default:<__main__.ElectricCar object at 0x22ff14>--->display object memory location
class Point3D(object):
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __repr__(self):
        print "(%d, %d, %d)" % (self.x,self.y,self.z)
myPoint = Point3D(1,2,3)
myPoint.__repr__()