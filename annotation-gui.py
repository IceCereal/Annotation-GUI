"""
	Annotater Driver for Annotation task.
	Objective: To annotate the phrases in 'Source*.csv'
"""
print ("Annotation - GUI")

import csv
import sys
import json
import subprocess

from os import mkdir
from os import listdir
from os.path import isfile, join
from datetime import datetime
from ast import literal_eval as le

# LOGGER FUNCTION
def writeLog(writeData : str):
	with open("Logger.txt", 'a') as FLog:
		FLog.write("\n"+str(datetime.now())+"\t"+writeData.upper())

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
				writeLog("FOUND AND COPIED SOURCE TO SOURCEEDITABLE")
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

# IMPORT NLTK ATTEMPT#1
try:
	import nltk
	writeLog("NLTK#1 IMPORTED")
except:
	try:
		subprocess.run(['pip', 'install', 'nltk']) # PIP INSTALL (PIP3 DOESN'T EXIST)
		writeLog("PIP INSTALL NLTK: SUCCESS")
	except:
		subprocess.run(['pip3', 'install', 'nltk']) # PIP3 INSTALL (PIP DOESN'T EXIST)
		writeLog("PIP3 INSTALL NLTK: SUCCESS")

# IMPORT NLTK ATTEMPT#2
try:
	import nltk
	writeLog("NLTK#2 IMPORTED")
except:
	print ("ERROR1: NLTK\n\nEXIT")
	writeLog("IMPORT NLTK: FAIL! SYS EXIT")
	sys.exit()

# IMPORT PYGAME ATTEMPT#1
try:
	import pygame as pg
	writeLog("PYGAME#1 IMPORTED")
except:
	try:
		subprocess.run(['pip', 'install', 'pygame']) # PIP INSTALL (PIP3 DOESN'T EXIST)
		writeLog("PIP INSTALL PYGAME: SUCCESS")
	except:
		subprocess.run(['pip3', 'install', 'pygame']) # PIP3 INSTALL (PIP DOESN'T EXIST)
		writeLog("PIP3 INSTALL PYGAME: SUCCESS")

# IMPORT PYGAME ATTEMPT#2
try:
	import pygame as pg
	writeLog("PYGAME#2 IMPORTED")
except:
	print ("ERROR1: PYGAME\n\nEXIT")
	writeLog("IMPORT PYGAME: FAIL! SYS EXIT")
	sys.exit()

# ATTEMPT TO DOWNLOAD NLTK.WORDNET
try:
	nltk.download('wordnet')
except:
	print ("ERROR2: NLTK - DOWNLOAD\n\nEXIT")
	writeLog("DOWNLOAD NLTK.DOWNLOAD('WORDNET'): FAIL! SYS EXIT")
	sys.exit()

# IMPORT WORDNET
from nltk.corpus import wordnet

# THE LIST OF SYNONYMS THAT CONTAINS ALL FUTURE SYNONYMS
globalSynonymsList = []

# READ SOURCE EDITABLE / SOURCE
try:
	writeLog("TRY READING SOURCEEDITABLE")
	with open("SourceEditable.csv", 'r') as Fobj:
		reader = csv.reader(Fobj)

		for row in reader:
			globalSynonymsList.append((row[0], row[1], row[2]))
	writeLog("SUCCESS READING SOURCEEDITABLE")
except:
	try:
		writeLog("TRY READING SOURCE")
		with open(fileNameOrigSource, 'r') as Fobj:
			reader = csv.reader(Fobj)

			for row in reader:
				globalSynonymsList.append((row[0], row[1], row[2]))
		writeLog("SUCCESS READING SOURCE")
	except:
		print ("ERROR3: READING SOURCE FILE\n\nEXIT")
	
		writeLog("READING SOURCE FILE: FAIL! SYS EXIT")
		sys.exit()

synonymsTotal = [] 
relSynonyms = []

# INSTRUCTIONS
writeLog("BEGIN INSTRUCTIONS")
print (	"\nInstructions:"
	"\nIf you misspell a word, please continue. There is no back button."
	"\nIf you select any wrong option and click next, please continue."
	"\nIf you quit at any time, you can continue by running this program again from where you left off."
	"\nIf there are any issues, please contact NS Raghav: raghav170555@mechyd.ac.in"
	"\n\nPlease hit enter to continue."
	)
inp = input()
writeLog("INPUT RECEIVED INSTRUCTIONS:\t" + inp)

# PYGAME INITIALIZED
pg.init()
pg.display.set_caption("Annotation")
screen = pg.display.set_mode((800,800))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('green')
FONT = pg.font.Font(None, 32)

# GET SYNONYMS THROUGH WORDNET
def getSyns(syn):
	synonymsTotal = []
	for synonym in wordnet.synsets(syn):
		for l in synonym.lemmas(): 
			synonymsTotal.append(l.name()) 

	synonymsTotal = list(set(synonymsTotal))

	if syn in synonymsTotal:
		synonymsTotal.remove(syn)

	return synonymsTotal

# INPUT TEXT BOX
class InputBox:

	def __init__(self, x, y, w, h, text=''):
		self.rect = pg.Rect(x, y, w, h)
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = FONT.render(text, True, self.color)
		self.active = False

		self.flag = 0
		
	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False

			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_RETURN:
					ls = []
					
					ls = getSyns(self.text)
					ls.append(self.text)

					with open("Temp.txt", 'w') as Fobj:
						Fobj.write(str(ls))
					
					self.text = ''
					self.flag = 1
				
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				
				else:
					self.text += event.unicode

				self.txt_surface = FONT.render(self.text, True, self.color)

	def update(self):
		width = max(200, self.txt_surface.get_width()+10)
		self.rect.w = width

	def draw(self, screen):
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		pg.draw.rect(screen, self.color, self.rect, 2)

# IF A BUTTON IS CLICKED
def buttonClick(msg,x,y,w,h,ic,ac, listOfSynsChosen=None, finiale = None, unclick = None, lastClick = None):
	mouse = pg.mouse.get_pos()
	click = pg.mouse.get_pressed()
	
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pg.draw.rect(screen, ac,(x,y,w,h))

		if click[0] == 1:
			if finiale == True:
				return True
			
			if msg not in listOfSynsChosen:
				listOfSynsChosen.append(msg)
				return True
			
			if unclick == True:
				try:
					listOfSynsChosen.remove(msg)
				except:
					pass
				return True
			
	else:
		pg.draw.rect(screen, ic,(x,y,w,h))

	message = myfont.render(msg, 1, pg.Color("White"))
	screen.blit( message, (x+w, y) )

# DRAW BUTTON: NO-CLICK
def drawButton(msg,x,y,w,h,ic,ac, listOfSynsChosen=None, finiale = None, unclick = None, lastClick = None):
	mouse = pg.mouse.get_pos()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pg.draw.rect(screen, ac,(x,y,w,h))
	
	else:
		pg.draw.rect(screen, ic,(x,y,w,h))
	
	message = myfont.render(msg, 1, pg.Color("White"))
	screen.blit (message, (x+w, y) )

# GLOBAL FONT
myfont = pg.font.SysFont("Serif", 20)

### MAIN DRIVER
def main(metaData):
	writeLog("ENTERED MAIN: INIT VARS")	

	clock = pg.time.Clock()
	input_box1 = InputBox(100, 200, 140, 32)
	input_boxes = [input_box1]
	done = False

	listOfSynsChosen = [] # List of chosen synonyms
	globalSynonymCounter = 0 # Synonym Counter
	tempFileDataHolder = '' # Data holder of Temp File

	btnFlag = 0
	btnColors = []

	buttonClickFlag = 0

	localCounter = 0

	writeLog("VARIABLES INITIALIZED")

	writeLog("BEGIN PROCESS:\t" + str(localCounter) +","+ str(globalSynonymsList[globalSynonymCounter][0]) +","+ str(globalSynonymsList[globalSynonymCounter][1]) +","+ str(globalSynonymsList[globalSynonymCounter][2]))

	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				writeLog("QUIT BUTTON ENCOUNTERED")
				done = True
			if  event.type == pg.MOUSEBUTTONDOWN:
				writeLog("CLICK ENCOUNTERED")
				if event.button == 1:
					buttonClickFlag = 1  

			for box in input_boxes:
				box.handle_event(event)

		for box in input_boxes:
			box.update()

		screen.fill((30, 30, 30))
		
		for box in input_boxes:
			box.draw(screen)

		
		header = myfont.render("#    UID    ADJ    NOUN", 1, pg.Color("White"))
		label = myfont.render(str(globalSynonymCounter+1)+"."+str(localCounter+1)+"    "+globalSynonymsList[globalSynonymCounter][0]+"    "+globalSynonymsList[globalSynonymCounter][1]+"    "+globalSynonymsList[globalSynonymCounter][2], 1, pg.Color("White"))
		altText = myfont.render("One Word Meanings of:   "+globalSynonymsList[globalSynonymCounter][1], 1, pg.Color("White"))
		screen.blit(header, (100, 20))
		screen.blit(altText, (100, 80))
		screen.blit(label, (100, 50))
		
		
		if input_box1.flag == 1:
			with open("Temp.txt", 'r') as Fobj:
				rawdata = Fobj.read()
				tempFileDataHolder = le(rawdata)

			x = 0

			if btnFlag == 0:
				for i in range(0,len(tempFileDataHolder)-1):
					btnColors.append(0)
				btnFlag = 1

			if (buttonClickFlag == 1):
				buttonClickFlag = 0
				for i in range(0,len(tempFileDataHolder)-1):
					if i > 20:
						break
					if btnColors[i] == 0:
						if (buttonClick(tempFileDataHolder[i],320,200+x,20,20,pg.Color("red"),pg.Color("yellow"), listOfSynsChosen, unclick=False)):
							btnColors[i] = 1
					else:
						if (buttonClick(tempFileDataHolder[i],320,200+x,20,20,pg.Color("green"),pg.Color("yellow"), listOfSynsChosen,unclick=True)):
							btnColors[i] = 0

					x += 21
			else:
				for i in range(0,len(tempFileDataHolder)-1):
					if i > 20:
						break
					if btnColors[i] == 0:
						if (drawButton(tempFileDataHolder[i],320,200+x,20,20,pg.Color("red"),pg.Color("yellow"), listOfSynsChosen, unclick=False)):
							btnColors[i] = 1
					else:
						if (drawButton(tempFileDataHolder[i],320,200+x,20,20,pg.Color("green"),pg.Color("yellow"), listOfSynsChosen,unclick=True)):
							btnColors[i] = 0

					x += 21

			if (buttonClick("Next",320,200+x, 20, 20, pg.Color("blue"),pg.Color("lightblue"), listOfSynsChosen=None, finiale=True,unclick=False )):
				try:
					listOfSynsChosen.append(tempFileDataHolder[i+1])
				except:
					listOfSynsChosen.append(tempFileDataHolder[0])
				print (listOfSynsChosen)
				localCounter += 1

				btnColors = []
				btnFlag = 0

				writeLog("NEXT BUTTON CLICKED. DATA IN LISTOFSYNSCHOSEN:\t" + str(listOfSynsChosen))

				if localCounter > 1:
					localCounter = 0

					writeLog("BEGIN: WRITING TO CAPTUREDDATA.CSV")
					with open("CapturedData.csv", 'a') as Fobj2:
						Fobj2.write("\n"+str(globalSynonymsList[globalSynonymCounter][0])+','+str(listOfSynsChosen))
					writeLog("COMPLETED: WRITING TO CAPTUREDDATA.CSV")

					writeLog("WRITE TO SOURCEALTS-CAPTUREDATA"+str(metaData["Sessions_Activated"])+".csv")
					try:
						writeLog("TRY: WRITE TO WINDOWS")
						with open("SourceAlts\\CapturedData"+str(metaData["Sessions_Activated"])+".csv", 'a') as Fobj:
							Fobj.write("\n"+str(globalSynonymsList[globalSynonymCounter][0])+','+str(listOfSynsChosen))
						writeLog("SUCCESS: WRITE TO WINDOWS")
					except:
						writeLog("TRY: WRITE TO LINUX/MACOS")
						with open("SourceAlts/CapturedData"+str(metaData["Sessions_Activated"])+".csv", 'a') as Fobj:
							Fobj.write("\n"+str(globalSynonymsList[globalSynonymCounter][0])+','+str(listOfSynsChosen))
						writeLog("SUCCESS: WRITE TO LINUX/MACOS")

					removeLineFlag = 0
					linesToWrite = []

					writeLog("UPDATE: SOURCEFILE.CSV")
					with open("SourceEditable.csv", 'r') as Fobj:
						reader = csv.reader(Fobj)

						for line in reader:
							if removeLineFlag == 0:
								removeLineFlag = 1
								continue
							else:
								linesToWrite.append(line)

					with open("SourceEditable.csv", 'w') as Fobj:
						for line in linesToWrite:
							Fobj.write(line[0]+','+line[1]+','+line[2]+'\n')
					writeLog("UPDATED: UPDATING SOURCEFILE.CSV")

					writeLog("UPDATE METADATA_ANNOTATION.JSON")
					with open("metadata_annotation.json", 'r') as Fobj:
						metaDataRaw = Fobj.read()
						metaData = json.loads(metaDataRaw)
					metaData["WordsCompleted"] += 1
					with open("metadata_annotation.json", 'w') as Fobj:
						metaDataJson = json.dumps(metaData)
						Fobj.write(metaDataJson)
					writeLog("UPDATED: METADATA_ANNOTATION.JSON")
					
					globalSynonymCounter += 1
					listOfSynsChosen = []

				input_box1.flag = 0

		pg.display.flip()

		clock.tick(60)

# UPDATE METADATA_ANNOTATION.JSON
writeLog("UPDATE: METADATA_ANNOTATION.JSON")
metaData["Sessions_Activated"] += 1
if name not in metaData["Names"]:
	metaData["Names"].append(name)
with open("metadata_annotation.json", 'w') as Fobj:
	metaDataJson = json.dumps(metaData)
	Fobj.write(metaDataJson)
writeLog("UPDATED: METADATA_ANNOTATION.JSON")

writeLog("BEGIN MAIN")
try:
	main(metaData)
except Exception as e:
	writeLog("ENCOUNTERED EXCEPTION: "+str(e))
	print ("ENCOUNTERED ERROR:\t"+str(e))
	print ("Please try launching the program again, and if this error persists, please contact NS Raghav: raghav170555@mechyd.ac.in")
pg.quit()

writeLog("USER EXIT")

print ("Thank you! If you have completed the Annotation, please follow the instructions. If not, you can re-run the program and you will continue from where you left.")