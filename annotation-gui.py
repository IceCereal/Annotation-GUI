"""
	Annotater Driver for Annotation task.
	Objective: To annotate the phrases in 'Source*.csv'
"""
print ("Annotation - GUI")

import sys
import json
import subprocess

from os import mkdir
from os import listdir
from os.path import isfile, join
from datetime import datetime

# LOGGER FUNCTION
def writeLog(writeData : str):
	with open("Logger.txt", 'a') as FLog:
		FLog.write("\n"+str(datetime.datetime.now())+"\t"+writeData.upper())

writeLog("\n\nBEGIN SESSION")

# CREATE SOURCEEDITABLE.CSV IF IT DOESN'T EXIST
def makeSourceEditable():
	writeLog("BEGIN: MAKE SOURCEEDITABLE")
	
	tempFileNameHolder = ''
	
	for fileName in filesInDir:
		if "source" in fileName.lower():
			try:
				writeLog("PRESUMING LINUX/MACOS... TRYING CP")
				subprocess.run(['cp', fileName, 'SourceEditable.csv'], shell=True)
				writeLog("FOUND AND COPIED SOURCE TO SOURCEEDITABLE")
			except:
				pass	

			writeLog("PRESUMING WINDOWS... SHIFTING FROM CP TO COPY")

			try:
				subprocess.run(['copy', fileName, 'SourceEditable.csv'], shell=True)
				writeLog("FOUND AND COPIED SOURCEFILE TO SOURCEEDITABLE")
			except:
				writeLog("COPY SOURCE TO SOURCEEDITABLE: FAILED! ASKING FOR MANUAL COPY & RENAME")
				
				print ("There was an error with the Program. For the program to run, please:\n\n1. Create a copy of:\t"+fileName+"\n2. Rename the Copy to:\t SourceEditable.csv\n\nHit Enter")
				
				understandInput = input()
				if understandInput == '\n':
					writeLog("INPUT RECEIVED UNDERSTANDINPUT:\tENTER")
				else:
					writeLog("INPUT RECEIVED UNDERSTANDINPUT:\t" + understandInput)
				
				writeLog("SYS EXIT")
				sys.exit()
			
			tempFileNameHolder = fileName

	writeLog("COMPLETE: MAKE SOURCEEDITABLE")
	
	return tempFileNameHolder