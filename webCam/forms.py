from django import forms

class photoForm(forms.Form):
  iso = forms.IntegerField(label='ISO', initial=800)
  shutterspeed = forms.FloatField(label='Shutter Speed', initial=6.0)