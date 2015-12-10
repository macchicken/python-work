import sys,traceback,Tkinter,UIItems
from DataResource import FinanceResource


class YahooFinance:
	
	def __init__(self,tkRoot):
		self.master = tkRoot
		self.master.protocol("WM_DELETE_WINDOW", self.exitClient)
		self.createWidgets()
		self.baseurl = "http://query.yahooapis.com/v1/public/yql?"

	def createWidgets(self):
		self.setup = Tkinter.Button(self.master, width=20, padx=3, pady=3)
		self.setup["text"] = "Currency"
		self.setup["command"] = self.getCurrency
		self.setup.grid(row=1, column=0, padx=2, pady=2)
		
		self.v = Tkinter.StringVar()
		self.label = Tkinter.Label(self.master, height=19, textvariable=self.v)
		self.label.grid(row=0, column=0, columnspan=5, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S, padx=5, pady=5)
		
	def getCurrency(self):
		try:
			inputd = UIItems.DialogWithOptions(self.master)
			if inputd.result is not None:
				first,second = inputd.result
				currencies=UIItems.getCurrencyShort(first),UIItems.getCurrencyShort(second)
				with FinanceResource(currencies) as reso:
					results = reso['query']['results']
					if results['rate']['Date'] == "N/A": self.v.set("no specific currency in the database at the moment")
					else: self.v.set("Name: %s, Rate: %s on %s %s" % (results['rate']['Name'],results['rate']['Rate'],results['rate']['Date'],results['rate']['Time']))
		except:
			print "\n"
			traceback.print_exc(file=sys.stdout)

	def exitClient(self):
		self.master.destroy()


if __name__ == "__main__":
	root = Tkinter.Tk()
	YahooFinance(root).master.title("Yahoo Finance")
	root.mainloop()