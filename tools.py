import os
import json
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
homeDir = os.path.expanduser('~')

def getKey(key, file='Default'):
  if file == 'Default':
    file = homeDir + '/.keys/keys'
  with open(file) as df:
    d = json.load(df)
  return d[key]

def onGPIO(pinNo, duration=60):

  try:
    GPIO.output(pinNo, True)
  except:
    raise
    # Set up the GPIO pin as an output.
    #GPIO.setup(pinNo, GPIO.OUT)
    #GPIO.output(pinNo, True)
  if duration > 0:
    time.sleep(duration)
    GPIO.output(pinNo, False)
  

