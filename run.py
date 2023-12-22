from testing import test
from app import App, startApplication
TESTING = False
BUILD = True

if TESTING:
	newTest = test
	print("Test start")
	newTest.Start()
	print("Test end")

if BUILD:
	startApplication()