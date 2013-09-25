import RPi.GPIO as GPIO
import time
import os
import sys
from morseDict import *



class Run(object):
	def __init__(self,output_pin=25,input_pin=18,message=None):
		with MorseMessage(output_pin=output_pin,input_pin=input_pin) as fd:
			if self.message: fd.write(message):
				for message in fd.read():fd.sendMessage(message)

class MorseMessage(object):
	def __init__(self, output_pin=25,input_pin=18):
		self.output_pin = output_pin
		self.input_pin = input_pin
		self.iSpeed = .005
		self.mark = 0
		self.message=[]
		word=''
		endKey = False
		return self

	def __enter__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(25,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(18, GPIO.BOTH, callback=self.lightReading)  
		return self

	def __exit__(self,xclass,xclassstr,xstacktrace):
		GPIO.cleanup()
		return self

	def sendMessage(self,message):
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
		self.endMessage()

	def endMessage(self):
	#	lightOn(iSpeed * 9)
		self.lightOn(iSpeed)
		time.sleep(iSpeed)
		self.lightOn(iSpeed)
		time.sleep(iSpeed)
		self.lightOn(iSpeed)
		time.sleep(iSpeed)
		self.lightOn(iSpeed*3)
		time.sleep(iSpeed)
		self.lightOn(iSpeed)
		time.sleep(iSpeed)
		self.lightOn(iSpeed*3)
		time.sleep(iSpeed)


	def lightReading(self,channel):
		lightValue = GPIO.input(channel)
		if time.time() - self.mark > 12 * iSpeed:
			self.message=[]
			self.word=''
			self.endKey =False
	 	startRead = True
		if startRead:		
			if not lightValue:
				if time.time()-self.mark >= 1.5*iSpeed and time.time()-self.mark < 5*iSpeed:
					self.word+='-'
				elif time.time()-self.mark < 1.5*iSpeed:
					self.word+='.'
			if self.word == '...-.-':
				print self.word
				self.endKey  = True
				self.word=''
			if time.time()-self.mark >1.5*iSpeed and len(self.word)>0 and lightValue:
				self.message.append(self.word)
				self.word=''
			if time.time()-self.mark > iSpeed * 5 and len(self.message)>0 and lightValue:
				self.message.append(' ')
			if time.time()-self.mark >= iSpeed * 8 and len(self.message)>0 or self.endKey :
				print self.morseProcess(self.message)
				self.message=[]
				self.word=''
				self.endKey =False
		self.mark = time.time()


	def morseProcess(self,morseList):
		totalMessage = ''
		for morse in morseList:
			if morse == ' ':
				totalMessage += ' '
			else:
				letter = [ key for key,val in morsetab.items() if val==morse ]
				totalMessage += letter[0]
		return totalMessage

	def lightOn(self,timeInterval=-1):
		GPIO.output(25,False)
		if (timeInterval!=-1):
			time.sleep(timeInterval)
			GPIO.output(25,True)

	def lightOff(self,timeInterval=-1):
		GPIO.output(25,True)
		if (timeInterval!=-1):
			time.sleep(timeInterval)
			GPIO.output(25,False)


