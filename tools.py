import os
import json
import time
import RPi.GPIO as GPIO
from picamera import PiCamera
from fractions import Fraction
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

def initCamera(mode='default'):
  if mode == 'lowlight':
    cam = PiCamera(resolution=(1280, 720), framerate=Fraction(1,6))
    cam.shutter_speed = 6000000 # 6 seconds is the maximum
    cam.iso = 800
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    time.sleep(30)
    cam.exposure_mode = 'off'
  else:
    cam = PiCamera()
    cam.start_preview()
    time.sleep(2)
  return cam

def closeCamera(cam):
  cam.stop_preview()

def takePhoto(cam, fileName='image.jpg'):
  cam.capture(fileName)
  return fileName

def takeLowLightPhoto():
  # turn on the lights.
  onGPIO(7, duration=40)
  # inititialize the camera.
  cam = initCamera(mode='lowlight')
  takePhoto(cam)


if __name__ == '__main__':
  takeLowLightPhoto()