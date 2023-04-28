from django import forms
  
# import GeeksModel from models.py
from .models import Event, Signal

# create a ModelForm
class RumorForm(forms.ModelForm):
    """
    A class to create Rumor form
    """
    def __init__(self, *args, **kwargs):
        super(RumorForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = ('Select')
    

    class Meta:
        model   = Signal
        fields  = ('status', 'contact', 'channel')

        widgets = {
            'contact': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'contact', 'placeholder': 'Write phone...' }),
            'status': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'status', 'required': '' }),
            'channel': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'channel', 'required': '' }),
        }

        labels = {
            'contact': 'Phone',
            'status': 'Status',
            'channel': 'Channel',
        }
  

class EventForm(forms.ModelForm):
    """
    A class to create Event form
    """
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['pri_sector'].empty_label = ('Select')
        self.fields['alert'].empty_label      = ('Select')

        self.fields['title'].required           = True
        self.fields['description'].required     = True
        self.fields['alert'].required           = True
        self.fields['pri_sector'].required      = True
    

    class Meta:
        model   = Event
        fields  = ('title', 'description', 'contact_name','contact_phone', 'pri_sector', 'alert')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'title', 'placeholder': 'Write title...', 'required': '' } ),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'title', 'placeholder': 'Write description...', 'rows': 3, 'required': '' }),
            'contact_name': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'contact_name', 'placeholder': 'Write full name...' }),
            'contact_phone': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'contact_phone', 'placeholder': 'Write phone...' }),
            'pri_sector': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'pri_sector', 'required': '' }),
            'alert': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-2.5 px-4 mb-3 my-1 focus:outline-none focus:border-none focus:bg-white text-sm font-normal', 'id': 'alert', 'required': '' }),
        }

        labels = {
            'title': 'Alert Title',
            'description': 'Description',
            'contact_name': 'Full name',
            'contact_phone': 'Phone',
            'pri_sector': 'Primary Sector',
            'alert': 'Alert Type',
            # 'sector': 'Involved Sectors'
        }


    
