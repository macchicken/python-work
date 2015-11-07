import tkMessageBox,sys,traceback
import urllib2,Tkinter,urllib,json,tkSimpleDialog

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
		inputd = MyDialog(self.master)
		first,second = inputd.result
		queryurl = urllib.urlencode({'q':'select * from yahoo.finance.xchange where pair in ("'+first.upper()+second.upper()+'")'})
		request = self.baseurl + queryurl + "&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
		conn = urllib2.urlopen(request)
		data = json.loads(conn.read())
		results = data['query']['results']
		conn.close()
		if results['rate']['Date'] == "N/A": self.v.set("no specific currency in the database at the moment")
		else: self.v.set("Name: %s, Rate: %s on %s %s" % (results['rate']['Name'],results['rate']['Rate'],results['rate']['Date'],results['rate']['Time']))

	def exitClient(self):
		self.master.destroy()


if __name__ == "__main__":
	root = Tkinter.Tk()
	YahooFinance(root).master.title("Yahoo Finance")
	root.mainloop()