import yahooConstants,Tkinter

master = Tkinter.Tk()

var = Tkinter.StringVar(master)
var.set("Afghan Afghani (AFN)") # initial value
var2 = Tkinter.StringVar(master)
var2.set("Afghan Afghani (AFN)") # initial value
OPTIONS=yahooConstants.Currencies.keys()
# option = OptionMenu(master, var, "one", "two", "three", "four")
option = apply(Tkinter.OptionMenu, (master, var) + tuple(OPTIONS))
option.pack()
option2 = apply(Tkinter.OptionMenu, (master, var2) + tuple(OPTIONS))
option2.pack()


# test stuff

def ok():
	v=var.get()
	v2=var2.get()
	print "value is %s, short %s" % (v,yahooConstants.Currencies[v])
	print "value is %s, short %s" % (v2,yahooConstants.Currencies[v2])
	

button = Tkinter.Button(master, text="OK", command=ok)
button.pack()

Tkinter.mainloop()