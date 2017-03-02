from django import forms

class photoForm(forms.Form):
  iso = forms.IntegerField(label='ISO', default=800)
  shutterspeed = forms.FloatField(label='Shutter Speed', default=6.0)