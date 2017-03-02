from django import forms

class photoForm(forms.Form):
  iso = forms.ChoiceField(label='ISO', choices=[100, 200, 300, 400, 500, 600, 700, 800], initial=800)
  shutterspeed = forms.FloatField(label='Shutter Speed', initial=6.0)