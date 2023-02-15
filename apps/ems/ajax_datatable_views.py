from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturalday
from .models import Event, Signal
import json
from django.forms.models import model_to_dict

class PermissionAjaxDatatableView(AjaxDatatableView):

    model = Permission
    title = 'Permissions'
    initial_order = [["app_label", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'codename', 'visible': True, },
        {'name': 'name', 'visible': True, 'className':'text-left text-green-800 font-medium' },
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]

class EventList(AjaxDatatableView):
    model                       = Event
    title                       = 'Alerts'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'alert', 'foreign_field': 'alert__reference', 'visible': True, 'className':'w-10 text-left'  },
        {'name': 'title', 'visible': True,'className':'text-left text-green-800 font-medium' },
        {'name': 'pri_sector', 'foreign_field': 'pri_sector__title', 'title': 'Sector', 'visible': True,'className':'w-36 text-left' },
        {'name': 'location', 'foreign_field': 'location__title','visible': True,'max_length': 15, 'className':'w-36 text-left' },
        {'name': 'stage', 'foreign_field': 'stage__title','visible': True, 'className':'w-32 text-left'  },
        {'name': 'created_on', 'title':'Created','visible': True, 'className':'w-[100px] text-left'  },
        {'name': 'updated_on','title':'Updated','visible': True, 'className':'w-[100px] text-left'  },
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        row['title'] = '<a href="%s">%s</a>' % (
            reverse('event', args=(obj.id,)),
            obj.title
        )
        row['created_on']   = naturalday(obj.created_on)
        row['updated_on']   = naturalday(obj.updated_on)
        
        

class RumorList(AjaxDatatableView):
    model                       = Signal
    title                       = 'Rumors'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[11, 50, 100, -1], [11, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'contents', 'title':'Contents','visible': True, 'className':'text-left flex-1 cursor-pointer'  },
        #{'name': 'contents', 'title':'Contents','visible': True, 'className':' text-left'  },
        {'name': 'css_icon', 'title':'','visible': True, 'className':'w-4 text-left','searchable': False,  },
        {'name': 'relevance', 'title':'#','visible': True, 'className':'w-4 text-left'  },
        {'name': 'created_on','title':'Updated','visible': True, 'className':'w-[90px] text-left'  },
        {'name': 'd','title':'','visible': True, 'className':'w-4 text-left','placeholder':'True','searchable': False,},
    ]
    
    def get_show_column_filters(self, request):
        return False
    
    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        #row['title'] = '<a href="%s">%s</a>' % (
        #    reverse('event', args=(obj.id,)),
        #    obj.title
        #)
        row['contents']     = '<span class=" line-clamp-1" @click="sidebarOpen = true, manageRumor('+str(obj.id)+')" >'+str(obj.contents['text'])+'</span>'
        row['css_icon']     = '<i class="'+obj.css_icon+'">'
        row['created_on']   = naturalday(obj.created_on)
        row['d']            = '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-200 hover:text-slate-500 hover:cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" @click="discardSignal('+str(obj.id)+')"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>'
        
    def get_initial_queryset(self, request=None):

        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method=='GET' else request.POST

        queryset = self.model.objects.all()

        if 'status' in request.REQUEST:
            status = request.REQUEST.get('status')
            queryset = queryset.filter(status=status)

        return queryset