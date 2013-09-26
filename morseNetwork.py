import RPi.GPIO as GPIO
import time
import os
import sys
from morseDict import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
iSpeed = .01

global startRead
global mark
global message
global word
global endKey
mark = 0
message=[]
word=''
endKey = False

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

def sendMessage(message):
	for c in message:
		if c==' ':
			time.sleep(iSpeed*4)
		else:
			morseMessage=morsetab[c]
			for m in morseMessage:
				if m=='.':
					lightOn(iSpeed)
				else: 	
					lightOn(iSpeed*3)
				time.sleep(iSpeed)
			time.sleep(iSpeed*2)
	endMessage()

def messageKey():
	time.sleep(iSpeed)
	lightOn(iSpeed)
	time.sleep(iSpeed)
	lightOn(iSpeed)

def endMessage():
#	lightOn(iSpeed * 10)
	lightOn(iSpeed)
	time.sleep(iSpeed)
	lightOn(iSpeed)
	time.sleep(iSpeed)
	lightOn(iSpeed)
	time.sleep(iSpeed)
	lightOn(iSpeed*3)
	time.sleep(iSpeed)
	lightOn(iSpeed)
	time.sleep(iSpeed)
	lightOn(iSpeed*3)
	time.sleep(iSpeed)


def lightReading(channel):
	global mark
	global message
	global word
	global endKey 
	lightValue = GPIO.input(channel)
	if time.time() - mark > 15 * iSpeed:
		message=[]
		word=''
		endKey=False
 	startRead = True
	if startRead:		
		if not lightValue:
			if time.time()-mark >= 1.5*iSpeed and time.time()-mark < 5*iSpeed:
				word+='-'
			elif time.time()-mark < 1.5*iSpeed:
				word+='.'
		if word == '...-.-':
			endKey = True
			word=''
		if time.time()-mark >1.5*iSpeed and len(word)>0 and lightValue:
			message.append(word)
			word=''
		if time.time()-mark > iSpeed * 6 and len(message)>0 and lightValue:
			message.append(' ')
		if time.time()-mark >= iSpeed * 10 and len(message)>0 or endKey:
			morseProcess(message)
			message=[]
			word=''
			endKey=False
	mark = time.time()


def morseProcess(morseList):
	totalMessage = ''
	for morse in morseList:
		if morse == ' ':
			totalMessage += ' '
		elif morse == '...-.-':
			totalMessage += ''
		else:
			letter = [ key for key,val in morsetab.items() if val == morse ]
			totalMessage += letter[0]
	if 'L' in totalMessage[:1]: 
		print totalMessage
	else:
		time.sleep(2)
		sendMessage(totalMessage)

def lightOn(timeInterval=-1):
	GPIO.output(25,False)
	if (timeInterval!=-1):
		time.sleep(timeInterval)
		GPIO.output(25,True)

def lightOff(timeInterval=-1):
	GPIO.output(25,True)
	if (timeInterval!=-1):
		time.sleep(timeInterval)
		GPIO.output(25,False)

#def startReading():
try:
	GPIO.add_event_detect(18, GPIO.BOTH, callback=lightReading)
except:
	pass
