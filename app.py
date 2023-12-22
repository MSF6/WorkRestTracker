from trackActive import getForegroundWindowPID
from trackProcess import PNameByPID
from tkinter import *
from tkinter import ttk
from time import sleep
from datetime import timedelta
from threading import Thread
import json
import sys

class App(Tk):
	def __init__(self):
		super().__init__()
		self.installMainOptions()
		self.installStartingWidgets()
		self.installStartingValues()
		self.startThreads()

	def installMainOptions(self):
		self.exitFlag = False
		self.pauseFlag = False #For pause thread pause use in future
		self.loadSaveFile = True
		self.protocol("WM_DELETE_WINDOW", self.onQuit)
	def setLabelCurrentProcessText(self, text):
		self.labelCurrentProcess.config(text = "Current process: " + text)

	def installStartingValues(self):
		if self.loadSaveFile:
			try:
				with open("save.txt", "r") as saveF:
					self.sessionData = json.load(saveF)
				self.fillTableWithData()
			except:
				print("SAVE FILE NOT LOADED!")
				self.sessionData = {}
		else:
			self.sessionData = {}
	def Saved(self):
		# Check save file existance and return data from save, otherwise return False
		return False
	def startThreads(self):
		self.threads = []

		self.upd_thread = Thread(target = self.updateSessionInfo)
		self.threads.append(self.upd_thread)

		self.log_thread = Thread(target = self.log)
		self.threads.append(self.log_thread)


		for t in self.threads:
			t.start()
	def log(self, updateInterval = 1):
		while True:
			if not self.exitFlag:
				print(self.sessionData)
				sleep(updateInterval)
			else:
				return
	def installStartingWidgets(self):
		self.title("Activity tracker")
		self.geometry("600x250")
		self.iconbitmap(default = "WRTicon2.ico")

		self.labelCurrentProcess = ttk.Label(self, text = "None")
		self.tableProcessSession = ttk.Treeview(self, columns=('activeTime'))
		self.labelCurrentProcess.pack()
		self.installTableProcessSession()
	def installTableProcessSession(self):
		self.tableProcessSession.heading('#0', text = "Name")
		self.tableProcessSession.heading('#1',text =  "Active time")
		self.tableProcessSession.pack()
	def fillTableWithData(self):
		for process in self.sessionData:
			self.tableProcessSession.insert('','end', process, text = process, values = (timedelta(seconds = self.sessionData[process])))
	def saveSessionInfo(self):
		with open("save.txt", "w") as saveF:
			json.dump(self.sessionData, saveF)

	def updateSessionInfo(self, updateInterval = 1):
		try:
			while True:
				if not self.exitFlag:
					self.frontWindowProcess = PNameByPID(getForegroundWindowPID())
					self.setLabelCurrentProcessText(self.frontWindowProcess)
					if self.frontWindowProcess not in self.sessionData:
						self.sessionData[self.frontWindowProcess] = 0
						self.tableProcessSession.insert('','end', self.frontWindowProcess, text = self.frontWindowProcess, values = (timedelta(seconds = 0)))
					else: 
						self.sessionData[self.frontWindowProcess] += updateInterval
						self.tableProcessSession.set(self.frontWindowProcess, '#1', timedelta(seconds = self.sessionData[self.frontWindowProcess]))
					sleep(updateInterval)
				else: return
		except Exception as error:
		 	print("Exception: ", error)
	def onQuit(self):
		self.saveSessionInfo()
		self.exitFlag = True
		self.pauseFlag = True
		print("onQuit")
		self.destroy()



def startApplication():
	root = App()
	root.mainloop()
	print("mainloop done")
	sys.exit()

