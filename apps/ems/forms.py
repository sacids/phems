from django import forms
  
# import GeeksModel from models.py
from .models import Event
  
# create a ModelForm
class EventForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model   = Event
        fields  = ('title','description','alert', 'sector', 'contact_name', 'contact_email', 'contact_prof','contact_phone', 'location', 'signal')