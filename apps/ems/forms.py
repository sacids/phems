from django import forms
  
# import GeeksModel from models.py
from .models import Event
  
# create a ModelForm
class EventForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model   = Event
        fields  = ('description', 'sector', 'contact_name', 'contact_email', 'contact_prof', 'location', 'signal')