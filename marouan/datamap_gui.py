from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import *
from tkinter import ttk
from filescanner import mpt, find_files
import pandas as pd

class GUI(Tk):
#---Initialisation
	def __init__(self):
		Tk.__init__(self)
		self.title("GDPR Data Map v0.1")
		self.geometry("800x600")
		self['bg']= "#6C7A89"
		self.Accueil()

#---Fenêtre d'accueil : Titres
	def Accueil(self):
		Label(self, text="GDPR Data Map", font="Verdana 36 bold", bg="#6C7A89", \
			fg="white").pack(side=TOP)
		Label(self, text="Personal Data Mapping", \
			font=("Verdana", "14"), bg="white").pack(fill=X)
		Label(self, text="(c) Leon | Marouan | Thomas | Toon , december 2017, v0.1", \
			bd=1, relief=SUNKEN, anchor=W).pack(side=BOTTOM, fill=X)

#---Image de fond de la page d'accueil
		couverture = PhotoImage(file="./img/cover.gif")
		self.couverture = couverture
		L2 = Label(self, image=couverture, bg="#6C7A89")
		L2.pack(side=BOTTOM, anchor="se")

#---Boutons de la page d'accueil : "launch", "about", "quit"
		icones = ["./img/btn/launch.gif","./img/btn/about.gif","./img/btn/logout.gif"]
		launch, about, quitter = PhotoImage(file=icones[0]), \
		PhotoImage(file=icones[1]), PhotoImage(file=icones[2])
		self.launch, self.about, self.quitter = launch, about, quitter
		Button(self, text="Launch", image=launch, compound=LEFT, \
			command=self.choices).pack(side=LEFT, expand=1)
		Button(self, text="About", image=about, compound=LEFT, \
			command=self.apropos).pack(side=LEFT, expand=1)
		Button(self, text="Quit", image=quitter, compound=LEFT, \
			command=quit).pack(side=LEFT, expand=1)

#---About window
	def apropos(self):
		about = 'Some message to explain what is all about.\nSome text need to be written.'
		msg = showinfo('About', message='About this app', detail=about)
		return msg

#---Launch window
	def choices(self):
		self.l = Toplevel()
		self.l.title("Before starting...")
		
		fr1 = LabelFrame(self.l, text="Choose your language(s)")
		fr2 = LabelFrame(self.l, text="Choose your country")
		fr3 = LabelFrame(self.l, text="Choose your path")
		fr4 = Frame(self.l)
		fr1.grid(row=0, column=0, sticky=S)
		fr2.grid(row=0, column=1, sticky=S)
		fr3.grid(row=0, column=2, sticky=S)
		fr4.grid(row=1, columnspan=3)

		languages = ['French','Dutch','English','Deutsch']
		self.ch_lg = []
		for i, l in enumerate(languages):
			var = StringVar()
			chk = Checkbutton(fr1, text=l, onvalue=l, offvalue='', variable=var)
			chk.grid(row=i, column=0, sticky=W)
			chk.deselect()
			self.ch_lg.append(var)
		
		countries = ['BE', 'NL', 'LU', 'UK']
		self.ch_c = []
		for j, c in enumerate(countries):
			var_c = StringVar()
			chk_c = Checkbutton(fr2, text=c, onvalue=c, offvalue='', variable=var_c)
			chk_c.grid(row=j, column=0, sticky=W)
			self.ch_c.append(var_c)

		self.list_mpt = Listbox(fr3, height=len(mpt()), selectmode=SINGLE)
		self.list_mpt.grid(row=0)

		for m in mpt():
			self.list_mpt.insert(END,m['device'])		

		lab = Label(fr3, height=2, justify=LEFT)
		lab.grid(row=1, column=0, sticky=W)
		
		def selection(event):
			if self.list_mpt.curselection():
				tt = mpt()
				ind = int(self.list_mpt.curselection()[0])
				det1 = tt[ind]['mountpoint']
				det2 = tt[ind]['fstype']
				txt = 'mountpoint: '+det1+'\n'+'fstype: '+det2
				lab.config(text=txt)
				self.ch_pth = det1
			else:
				lab.config(text='')


		self.list_mpt.bind("<<ListboxSelect>>", selection)

		Button(fr4, text="Scan", command=self.scan_results).grid(padx=20, pady=20)

	def scan_results(self):
#		l1 = [x.get() for x in self.ch_lg]
#		l2 = [y.get() for y in self.ch_c]
		self.s = Toplevel()
#		progress = ttk.Progressbar(self.s, mode="indeterminate", length="100")
#		progress.pack()
#		progress.start()
		#path = self.ch_pth
		path = '/home/marouan/Bureau'
		df = find_files(path)
		nbr_found_files = df['filepath'].count()
		nbr_found_extensions = df['ext'].count()
		results = str(nbr_found_files)+' found files, including '+\
			str(nbr_found_extensions)+' with extension.'
		Label(self.s, text=results).pack()
#		progress.stop()
#		print ('done')




if __name__ == '__main__':
	GUI().mainloop()
