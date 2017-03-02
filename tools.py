import os
import json
import time
import sys
import RPi.GPIO as GPIO
from fractions import Fraction
homeDir = os.path.expanduser('~')

try:
  from picamera import PiCamera
  gotpicamera = True
except ImportError:
  gotpicamera = False

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
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pinNo, GPIO.OUT)
  GPIO.output(pinNo, False)
  GPIO.cleanup()

def initCamera(mode='default', iso='default', ss='default', tt='default'):
  if gotpicamera == False:
    print 'not got picamera'
    # raise error
    return
  if mode == 'default':
    cam = PiCamera()
    cam.start_preview()
    time.sleep(2)
  else:
    cam = PiCamera(resolution=(1280, 720), framerate=Fraction(1,6))
    #cam.color_effects = (128,128) # turn camera to black and white

    cam.shutter_speed = ss*1000000 # 6 seconds is the maximum
    cam.iso = iso
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    time.sleep(30) #(30)
    cam.exposure_mode = 'off'
  return cam

def closeCamera(cam):
  cam.stop_preview()

def takePhoto(cam, fileName='image.jpg'):
  cam.capture(fileName)
  return fileName

def takeLowLightPhoto():
  # turn on the lights.
  onGPIO(7, duration=-1)
  try:
    # inititialize the camera.
    cam = initCamera(mode='lowlight')
    # take the photo
    takePhoto(cam)
    # turn off the lights.
    offGPIO(7)
  except KeyboardInterrupt:
    offGPIO(7)

if __name__ == '__main__':
  args = sys.argv[1:]

  if args[0] == "takePhoto":
    # Get the arguments
    iso = int(args[args.index('--iso')+1])
    ss = int(args[args.index('--ss')+1])
    tt = args[args.index('--tt')+1]
    fn = args[args.index('--fn')+1]
    fn = fn

    # Turn on the LEDs
    onGPIO(7, duration=-1)
    # initialize the camera
    cam = initCamera(mode='Y', iso=iso, ss=ss, tt=tt)
    # take the photo
    takePhoto(cam, fileName=fn)
    # turn off the lights.
    offGPIO(7)
