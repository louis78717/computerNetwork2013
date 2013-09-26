import RPi.GPIO as GPIO
import time
import os
import sys
from morseDict import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
iSpeed = .05
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.OUT)

def sendMessage(message):
	messageKey()
	for c in message:
		if c==' ':
			time.sleep(iSpeed*3)
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
	lightOn(iSpeed*6)

def lightReading(totalTime):
	key1 = False
	key2 = False
	key3 = False
	startRead = False
	currentMark = 0
	currentGap = 0
	elasped = 0
	message=[]
	word=''
	for i in range(0,int(totalTime/iSpeed)):
		now=time.time()
		lightValue = readLight()
		if (key1 == True and key2 == True and key3 == True):
			startRead = True
		elif (lightValue < 50 and key1 == False):
			key1 = True
		elif (key1 == True and lightValue > 50 and key2 == False):
			key2 = True
		elif (key2 == True and lightValue < 50 and key3 == False):
			key3 = True
		else:
			key1 = False
			key2 = False
			key3 = False
		if startRead == True:
			if lightValue < 50:
				currentMark = currentMark + 1
				currentGap = 0		
			else:
				if currentMark >= 2:
					word+='-'
				elif currentMark == 1:
					word+='.'
				currentGap = currentGap + 1
				currentMark = 0
			if currentGap > 1 and len(word)>0:
				message.append(word)
				word=''
			if currentGap > 5:
				message.append(' ')
			if currentMark > 4:
				key1 = False
				key2 = False
				key3 = False
				startRead = False
				print morseProcess(message)
				currentMark = 0
				currentGap = 0
				word=''						
				message=[]						
		elasped=time.time()-now
		time.sleep(iSpeed-elasped)


def morseProcess(morseList):
	totalMessage = ''
	for morse in morseList:
		if morse == ' ':
			totalMessage += ' '
		else:
			letter = [ key for key,val in morsetab.items() if val==morse ]
			totalMessage += letter[0]
	return totalMessage

def lightOff(timeInterval=-1):
	GPIO.output(25,True)
	if (timeInterval!=-1):
		time.sleep(timeInterval)
		GPIO.output(25,False)

def lightOn(timeInterval=-1):
	GPIO.output(25,False)
	if (timeInterval!=-1):
		time.sleep(timeInterval)
		GPIO.output(25,True)


def readLight():
	reading = 0
	GPIO.setup(18,GPIO.IN)
	while (GPIO.input(18) == GPIO.LOW):
		reading += 1
	GPIO.setup(18,GPIO.OUT)
	GPIO.output(18,GPIO.LOW)
	return reading	

