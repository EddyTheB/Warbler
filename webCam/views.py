from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import paramiko
from tools import getKey

from .models import Computer, Camera, Image


# Create your views here.
def index(request):
  return HttpResponse("Hello world! Index.")

def imageViewer(request, camID):

  # get the camera
  camera = get_object_or_404(Camera, pk=camID)

  # get the computer
  computer = get_object_or_404(Computer, pk=camera.computer_id)

  # create a filename to save to.
  fname = "image.jpg"

  # connect to the computer
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())   # Shouldn't be neccesary, don't know why it doesn't recognise host.
  ssh.connect(computer.ip_address, username=computer.user_name, password=getKey(computer.user_name))
  stdin, stdout, stderr = ssh.exec_command("cd Documents/Development/; python tools.py takeNightPhoto {}".format(fname))
  # Some sort of error handling would be good...
  #  print stderr.read()

  # Now copy the file locally.
  sftp = ssh.open_sftp()
  sftp.get("Documents/Development/{}".format(fname), "webCam/static/webCam/images/blah.jpg")
  sftp.close()
  ssh.close()
  # 

  return render(request, 'webCam/imageViewer.html', {'Address': 'blah.jpg'})
