from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

import paramiko
from datetime import datetime
from time import sleep


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
      iso = form.cleaned_data['iso']
      ss = form.cleaned_data['shutterspeed']

      # get the camera
      camera = get_object_or_404(Camera, pk=camID)

      # get the computer
      computer = get_object_or_404(Computer, pk=camera.computer_id)

      # Get the current date time
      d = datetime.now()
      dt_file = d.strftime('%y%m%d_%H%M%S')
      dt_text = d.strftime('%H:%M:%S_-_%a_%d_%b_%Y')
      dt_mysql = d.strftime('%Y-%m-%d %H:%M:%S %z')

      # create a filename to save to.
      fname = "Cam{}_{}.jpg".format(camID, dt_file)

      # Add all of those details to the database.
      print 'aaaaaaaa'
      I = Image(camera=camera, filename=fname, exdate=dt_mysql, shutterspeed=ss, resw=720, resh=1280, text=dt_text)
      I.save()
      print 'bbbbbbb'

      # connect to the computer
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())   # Shouldn't be neccesary, don't know why it
                                    # doesn't recognise host.
      ssh.connect(computer.ip_address, username=computer.user_name, password=getKey(computer.user_name))

      command = "cd Documents/Development/; python tools.py takePhoto --iso {} --ss {} --tt {} --fn {} --resw 720 --resh 1280".format(iso, ss, dt_text, fname)
      stdin, stdout, stderr = ssh.exec_command(command)
      # Some sort of error handling would be good...
      #  print stderr.read()

      # Wait for long enough for the photo to be taken.
      sleep(45)

      # Now copy the file locally.
      sftp = ssh.open_sftp()
      getFile = "Documents/Development/{}".format(fname)
      putFile = "webCam/static/webCam/images/{}".format(fname)
      sftp.get(getFile, putFile)
      sftp.close()
      # Now delete the original
      command = "rm Documents/Development/{}".format(fname)
      stdin, stdout, stderr = ssh.exec_command(command)
      ssh.close()

      return render(request, 'webCam/imageViewer.html', {'camera': camID, 'address': fname, 'form': form})

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


