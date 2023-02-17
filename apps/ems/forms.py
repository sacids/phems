from django import forms
  
# import GeeksModel from models.py
from .models import Event
  
# create a ModelForm
class EventForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model   = Event
        fields  = ('title','description','alert', 'sector', 'contact_name', 'contact_email', 'contact_prof','contact_phone', 'location', 'signal')


class RumorForm(forms.Form):
    """
    A class to create rumor form
    """
    def __init__(self, *args, **kwargs):
        super(RumorForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'id': 'step', 'placeholder': 'Write step...',}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Write title...', 'rows': 2 }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Write description...', 'rows': 3 }),
            'alert_type_id': forms.TextInput(attrs={'class': 'form-control', 'id': 'flag', 'placeholder': 'Write flag...', }),
            'loca': forms.TextInput(attrs={'class': 'form-control', 'id': 'label', 'placeholder': 'Write label...', }),
            'pull': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pull', 'placeholder': 'Write pull...', }),
            'url': forms.TextInput(attrs={'class': 'form-control', 'id': 'url', 'placeholder': 'Write pull url...', }),
            'action': forms.TextInput(attrs={'class': 'form-control', 'id': 'action', 'placeholder': 'Write action...', }),
        } 

    #     labels = {
    #         'step': "Menu Step",
    #         'keyword': 'Keyword',
    #         'title': 'Title',
    #         'flag': 'Flag',
    #         'label': 'Label',
    #         'pull': 'Pull',
    #         'url': 'Pull URL',
    #         'action': 'Action',
    #     }      
