from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

import paramiko
from datetime import datetime


from tools import getKey

from .models import Computer, Camera, Image
from .forms import photoForm


# Create your views here.
def index(request):
  return HttpResponse("Hello world! Index.")


def imageViewer(request, camID):

  if request.method == 'POST':
    form = photoForm(request.POST)
    if form.is_valid():
      print 'a'
      print form.cleaned_data
      iso = form.cleaned_data.iso
      ss = form.cleaned_data.shutterspeed

      # get the camera
      camera = get_object_or_404(Camera, pk=camID)

      # get the computer
      computer = get_object_or_404(Computer, pk=camera.computer_id)

      # Get the current date time
      dt = datetime.now().strftime('%y%m%d_%H:%M:%S')
      print dt

      # create a filename to save to.
      fname = "Cam{}_{}.jpg".format(camID, dt)

      # connect to the computer
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())   # Shouldn't be neccesary, don't know why it
                                    # doesn't recognise host.
      ssh.connect(computer.ip_address, username=computer.user_name, password=getKey(computer.user_name))

      command = "cd Documents/Development/; python tools.py takePhoto --iso {} --ss {} --fn {}".format(iso, ss, fname)
      print command
      stdin, stdout, stderr = ssh.exec_command(command)
      # Some sort of error handling would be good...
      #  print stderr.read()

      # Now copy the file locally.
      sftp = ssh.open_sftp()
      sftp.get("Documents/Development/{}".format(fname), "webCam/static/webCam/images/blah.jpg")
      sftp.close()
      ssh.close()

      pass

  else:
    form = photoForm()

  return render(request, 'webCam/imageViewer.html', {'camera': camID, 'address': 'blahXXX.jpg', 'form': form})


  """

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

  return render(request, 'webCam/imageViewer.html', {'camera': camID, 'address': 'blahXXX.jpg', 'form': photoForm()})
  """

def get_photoForm(request):

  print 'DDDDDDDDDDDDDDD'

  if request.method == 'POST':
    form = photoForm(request.POST)
    if form.is_valid():
      print 'a'
      print form
      pass
    else:
      print 'b'

  else:
    print 'c'
    form = photoForm()

  return render(request, 'webCam/imageViewer.html', {'form': form})


