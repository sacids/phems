from django import forms
  
# import GeeksModel from models.py
from .models import Event
  
# create a ModelForm
class EventForm(forms.ModelForm):
    required_css_class = 'required'
    """
    A class to create Event form
    """
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['pri_sector'].empty_label = 'Select'
        self.fields['alert'].empty_label      = 'Select'
    

    class Meta:
        model   = Event
        fields  = ('title', 'description', 'contact_name','contact_phone', 'location', 'pri_sector', 'alert')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'title', 'placeholder': 'Write title...', 'required': '' } ),
            'description': forms.Textarea(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'title', 'placeholder': 'Write description...', 'rows': 3, 'required': '' }),
            'contact_name': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'contact_name', 'placeholder': 'Write full name...' }),
            'contact_phone': forms.TextInput(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'contact_phone', 'placeholder': 'Write phone...' }),
            'location': forms.Select(attrs={'class': 'get_location w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'location', 'required': '' }),
            'pri_sector': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'pri_sector', 'required': '' }),
            'alert': forms.Select(attrs={'class': 'w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'alert', 'required': '' }),
            # 'sector': forms.Select(attrs={'class': 'select2 select2-multiple multiple w-full bg-white text-gray-600 border border-gray-300 rounded py-3 px-4 mb-3 my-1 leading-tight focus:outline-none focus:bg-white focus:border-gray-600 text-sm font-normal', 'id': 'sector', 'data-placeholder': 'Select sector ...', 'multiple': 'multiple' }),
        }

        labels = {
            'title': 'Alert Title',
            'description': 'Description',
            'contact_name': 'Full name',
            'contact_phone': 'Phone',
            'location': 'Location',
            'pri_sector': 'Primary Sector',
            'alert': 'Alert Type',
            # 'sector': 'Involved Sectors'
        }


    
