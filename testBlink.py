import RPi.GPIO as GPIO
import time
import os
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)
iSpeed = .5

def Blink(numTime, speed):
	for i in range(0, numTime):
		lightOn()
		print readLight()
		time.sleep(speed)
		lightOff()
		print readLight()
		time.sleep(speed)
	GPIO.cleanup()

def messageKey():
	lightOn(iSpeed)
	lightOff(iSpeed)

def message1():
	messageKey()
	lightOn(iSpeed)
	lightOff(iSpeed)
	lightOn(iSpeed)
	lightOn(iSpeed)

def message2():
	messageKey()
	lightOff(iSpeed)
	lightOn(iSpeed)
	lightOff(iSpeed)
	lightOn(iSpeed)

def lightReading(totalTime):
	key1 = False
	key2 = False
	startRead = False
	messageLength = 4
	for i in range(0,int(totalTime/iSpeed)):
		now=time.time()
		lightValue = readLight()
		if (key1 == True and key2 == True):
			startRead = True
		elif (lightValue < 50 and key1 == False):
			key1 = True
		elif (key1 == True and lightValue > 50):
			key2 = True
		else:
			key1 = False
			key2 = False
		if (startRead == True):
			messageLength=messageLength-1
			if (lightValue < 50):
				print '1',
			else:
				print '0',
			if (messageLength<=0):
				print 'Message End'
				messageLength=4
				startRead=False
				key1=False
				ket2=False
		
		elasped=time.time()-now
		time.sleep(iSpeed-elasped)
	print 'Sampling End'


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
	GPIO.setup(18,GPIO.OUT)
	GPIO.output(18,GPIO.LOW)
	time.sleep(.1)

	GPIO.setup(18,GPIO.IN)
	while (GPIO.input(18) == GPIO.LOW):
		reading += 1
	return reading	

