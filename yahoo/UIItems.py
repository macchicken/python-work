import Tkinter,tkSimpleDialog,yahooConstants


OPTIONS=sorted(yahooConstants.Currencies.keys())

class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        Tkinter.Label(master, text="Currency from:").grid(row=0)
        Tkinter.Label(master, text="Currency to:").grid(row=1)

        self.e1 = Tkinter.Entry(master)
        self.e2 = Tkinter.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        self.result = first, second
		
class DialogWithOptions(tkSimpleDialog.Dialog):

    def body(self, master):
		self.var = Tkinter.StringVar(master)
		self.var.set("Afghan Afghani (AFN)") # initial value
		self.var2 = Tkinter.StringVar(master)
		self.var2.set("Afghan Afghani (AFN)") # initial value
		option = apply(Tkinter.OptionMenu, (master, self.var) + tuple(OPTIONS))
		option.pack()
		option2 = apply(Tkinter.OptionMenu, (master, self.var2) + tuple(OPTIONS))
		option2.pack()
		return option

    def apply(self):
        first = self.var.get()
        second = self.var2.get()
        self.result = first, second

def getCurrencyShort(fullName):
	return yahooConstants.Currencies[fullName] 