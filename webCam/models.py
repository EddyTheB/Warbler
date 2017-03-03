from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class Computer(models.Model):
  type = models.CharField(max_length=28)
  ip_address = models.GenericIPAddressField()
  name = models.CharField(max_length=20)
  description = models.CharField(max_length=140)
  location = models.CharField(max_length=70)
  user_name = models.CharField(max_length=30)

  def __str__(self):
    return 'name: {} - type: {}'.format(self.name, self.type)

class Camera(models.Model):
  computer = models.ForeignKey(Computer, on_delete=models.CASCADE)
  type = models.CharField(max_length=100)


class Image(models.Model):
  camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
  filename = models.ImageField()
  exdate = models.DateTimeField('exposure date')
  resw = models.IntegerField(default=1280)
  resh = models.IntegerField(default=720)
  shutterspeed = models.FloatField()
  aperture = models.FloatField(default=2.8)
  iso = models.IntegerField(default=100)
  text = models.CharField(max_length=200)
  status = models.CharField(max_length=9, choices=[("InPrep", "In Preperation"),
                                                   ("Ready", "Ready"),
                                                   ("Deleted", "Deleted")], default="InPrep")

  #@classmethod
  #def create(cls, camera, filename, exdate, shutterspeed, resw=1280, resh=720,
  #           aperture=2.8, iso=100, text='', status='InPrep'):
  #  image = cls(camera=camera, filename=filename, exdate=exdate, shutterspeed=shutterspeed,
  #              resw=resw, resh=resh, aperture=aperture, iso=iso, text=text, status=status)
  #  return image


