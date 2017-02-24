import os
import json
import time
import RPi.GPIO as GPIO
homeDir = os.path.expanduser('~')

def getKey(key, file='Default'):
  if file == 'Default':
    file = homeDir + '/.keys/keys'
  with open(file) as df:
    d = json.load(df)
  return d[key]

def onGPIO(pinNo, duration=60):
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pinNo, GPIO.OUT)
  GPIO.output(pinNo, True)
  try:
    if duration > 0:
      time.sleep(duration)
      GPIO.output(pinNo, False)
  except KeyboardInterrupt:
      GPIO.output(pinNo, False)      
  GPIO.cleanup()

def offGPIO(pinNo):
  GPIO.output(pinNo, False)
  GPIO.cleanup()

