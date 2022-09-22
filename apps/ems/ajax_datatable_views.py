from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturalday
from .models import Event

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
        {'name': 'name', 'visible': True, },
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]

class EventList(AjaxDatatableView):
    model                       = Event
    title                       = 'Alerts'
    show_column_filters         = False
    initial_order               = [["created_on", "desc"], ]
    length_menu                 = [[20, 50, 100, -1], [20, 50, 100, 'all']]
    search_values_separator     = '+'
    full_row_select             = False
    
      
    
    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'alert', 'foreign_field': 'alert__reference', 'visible': True, 'className':'w-10 text-left'  },
        {'name': 'title', 'visible': True,'className':'text-left text-green-800' },
        {'name': 'pri_sector', 'foreign_field': 'pri_sector__title', 'title': 'Sector', 'visible': True,'className':'w-36 text-left' },
        {'name': 'location', 'foreign_field': 'location__title','visible': True,'max_length': 15, 'className':'w-36 text-left' },
        {'name': 'stage', 'foreign_field': 'stage__title','visible': True, 'className':'w-32 text-left'  },
        {'name': 'created_on', 'title':'Created','visible': True, 'className':'w-[87px] text-left'  },
        {'name': 'updated_on','title':'Updated','visible': True, 'className':'w-[87px] text-left'  },
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