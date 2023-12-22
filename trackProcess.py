import psutil

def getProcessNames():
	names = []
	for proc in psutil.process_iter():
		names.append(proc.name())
	return names

def PNameByPID(pid):
	for p in psutil.process_iter():
		if p.pid == pid:
			return p.name()
	return "No active processes with pid {}".format(pid)
	
