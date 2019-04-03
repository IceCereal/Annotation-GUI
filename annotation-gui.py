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

# ORIGINAL FILE NAME: SOURCE*.CSV
fileNameOrigSource = ''

# FIND ALL THE FILES IN THE CURRENT DIRECTORY
filesInDir = [f for f in listdir('.') if isfile(join('.', f))]

# LOOK/CREATE SOURCEEDITABLE.CSV
writeLog("LOOKING FOR SOURCEEDITABLE.CSV")
if "SourceEditable.csv" not in filesInDir:
	fileNameOrigSource = makeSourceEditable()
writeLog("FOUND/COMPLETED: SOURCEEDITABLE")

# METADATA STRUCTURE
metaData = {
	"Sessions_Activated" : 0,
	"OriginalSourceFileName": None,
	"WordsCompleted" : 0,
	"Names" : []
}

# LOOK/CREATE METADATA_ANNOTATION.JSON
writeLog("LOOKING FOR METADATA_ANNOTATION.JSON")
if "metadata_annotation.json" in filesInDir:
	with open("metadata_annotation.json", 'r') as Fobj:
		rawMetaData = Fobj.read()
		metaData = json.loads(rawMetaData)
		
		writeLog("METADATA_ANNOTATION.JSON LOADED")
	
else:
	writeLog("METADATA_ANNOTATION.JSON NOT FOUND")
	writeLog("CREATING METADATA_ANNOTATION.JSON")

	metaData["OriginalSourceFileName"] = fileNameOrigSource

	writeLog("CREATED METADATA_ANNOTATION.JSON")

# LOOK/CREATE SOURCEALTS/ OR SOURCEALTS\
writeLog("CREATE/LOOK FOR SOURCEALTS DIR")
try:
	mkdir("SourceAlts")
	writeLog("CREATED SOURCEALTS")
except:
	writeLog("LOCATED SOURCEALTS")

# GET NAME
print ("Welcome!")

print ("Please Enter Your Name:\t")
name = str(input())

writeLog("NAME:\t"+name)