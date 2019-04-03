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

def writeLog(writeData : str):
	with open("Logger.txt", 'a') as FLog:
		FLog.write("\n"+str(datetime.datetime.now())+"\t"+writeData.upper())

