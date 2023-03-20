from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturalday
from .models import Event, Signal
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group
from apps.notification.models import Notification
from datetime import date, datetime


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
        {'name': 'name', 'visible': True,
            'className': 'text-left text-green-800 font-medium'},
        {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
        {'name': 'model', 'foreign_field': 'content_type__model', 'visible': True, },
    ]

class UserList(AjaxDatatableView):
    model = User
    title = 'Manage Users'
    show_column_filters = False
    initial_order = [["first_name", "desc"], ]
    length_menu = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'first_name', 'title': 'Fullname', 'visible': True, 'className': 'w-36 text-left border-r'},
        {'name': 'email', 'visible': 'Email', 'className': 'w-32 text-left border-r'},
        {'name': 'username', 'visible': 'Username', 'className': 'w-20 text-left border-r'},
        {'name': 'roles', 'title': 'Roles','className': 'w-28 text-left border-r'},
        {'name': 'is_active', 'title': 'Status', 'visible': True, 'className': 'w-12 text-left border-r'},
        {'name': 'date_joined', 'title': 'Created On', 'visible': True,'className': 'w-[100px] text-left border-r'},
        {'name': 'last_login', 'title': 'Last Login', 'visible': True,'className': 'w-[100px] text-left border-r'},
        {'name': 'actions', 'title': '', 'visible': True, 'className': 'w-12 text-left', 'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        row['first_name'] = obj.first_name + " " + obj.last_name
        row['date_joined'] = naturalday(obj.date_joined)
        row['last_login'] = naturalday(obj.last_login)

        arr_roles = []

        if obj.groups.all():
            for val in obj.groups.all():
                arr_roles.append(val.name)
        row['roles'] = arr_roles

        if obj.is_active == True:
            row['is_active'] = '<span class="bg-green-600 text-white rounded-full px-2 py-0.5 text-xs font-medium">Active</span>' 
        elif obj.is_active == False:
            row['is_active'] = '<span class="bg-red-600 text-white rounded-full px-2 py-0.5 text-xs font-medium">Inactive</span>'

        row['actions'] = '<div class="flex">'\
                '<a href="%s" class="px-1">'\
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-slate-500 hover:text-blue-600 hover:cursor-pointer">'\
                    '<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />'\
                    '</svg>'\
                '</a>'\
                '<a href="%s" class="px-1">'\
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-500 hover:text-red-600 hover:cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">'\
                    '<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />'\
                    '</svg>'\
                '</a>'\
            '</div>' % (reverse('edit-user', args=(obj.id,)), reverse('delete-user', args=(obj.id,)))
        

class MessageList(AjaxDatatableView):
    model = Notification
    title = 'Notifications'
    show_column_filters = False
    initial_order = [["created_on", "asc"], ]
    length_menu = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'message', 'title': 'Message', 'visible': True, 'className': 'w-96 text-left border-r'},
        {'name': 'created_on', 'title': 'Created On', 'visible': True,'className': 'w-8 text-left border-r'},
        {'name': 'status', 'title': 'Status', 'visible': True, 'className': 'w-8 text-left border-r'},
        {'name': 'actions', 'title': '', 'visible': True, 'className': 'w-8 text-left border-r', 'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        row['created_on'] = obj.created_on.strftime('%d/%m/%Y %H:%M')

        if obj.app_status == 'PENDING':
            row['status'] = '<span class="bg-yellow-500 text-white rounded-full px-2 py-0.5 text-xs font-medium">Pending</span>'
            row['actions'] = '<a href="%s" class="px-1 py-1 rounded-sm text-white text-xs font-normal bg-gray-600">Mark as Read</a>' % reverse('mark-as-done', args=(obj.id,))

        elif obj.app_status == 'DELIVERED':
            row['status'] = '<span class="bg-green-600 text-white rounded-full px-2 py-0.5 text-xs font-medium">Delivered</span>'
            row['actions'] = ''   

        elif obj.app_status == 'REJECTED':
            row['status'] = '<span class="bg-red-400 text-white rounded-full px-2 py-0.5 text-xs font-medium">Rejected</span>'
            row['actions'] = ''

    def get_initial_queryset(self, request=None):
        queryset = super().get_initial_queryset(request)
        queryset = queryset.filter(user_id=request.user)
        return queryset
    
    

class EventList(AjaxDatatableView):
    model = Event
    title = 'Alerts'
    show_column_filters = False
    initial_order = [["created_on", "desc"], ]
    length_menu = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'alert', 'title': 'Alert Type', 'foreign_field': 'alert__label',
            'visible': True, 'className': 'w-36 text-left border-r'},
        {'name': 'title', 'visible': True, 'className': 'text-left w-max border-r'},
        {'name': 'pri_sector', 'foreign_field': 'pri_sector__title',
            'title': 'Primary Sector', 'visible': True, 'className': 'w-28 text-left border-r'},
        {'name': 'location', 'foreign_field': 'location__title', 'visible': True,
            'max_length': 15, 'className': 'w-36 text-left border-r'},
        {'name': 'stage', 'visible': True, 'className': 'text-left whitespace-nowrap w-20 border-r'},
        {'name': 'created_on', 'title': 'Created', 'visible': True,
            'className': 'w-[100px] text-left border-r'},
        {'name': 'actions', 'title': '', 'visible': True, 'className': 'w-10 text-left border-r',
            'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        row['title']        = '<a class="text-emerald-800 font-medium" href="%s">%s</a>' % (reverse('show-event', args=(obj.id,)), obj.title)
        row['created_on']   = naturalday(obj.created_on)
        row['stage']        = '<span class="rounded-md py-1 px-3 text-xs '+obj.stage.css+'">'+obj.stage.title+'</span>'
        
        if obj.status == 'NEW':
            row['status'] = '<span class="bg-blue-500 text-white rounded-full px-2 py-0.5 text-xs font-medium">New</span>'
            row['actions'] = '<div class="flex">'\
                '<a href="%s" class="px-1">'\
                    '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-slate-500 hover:text-blue-600 hover:cursor-pointer">'\
                    '<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />'\
                    '</svg>'\
                '</a>'\
                '<a href="%s" class="px-1">'\
                    '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-500 hover:text-red-600 hover:cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">'\
                    '<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />'\
                    '</svg>'\
                '</a>'\
            '</div>' % (reverse('edit-event', args=(obj.id,)), reverse('delete-event', args=(obj.id,)))

        elif obj.status == 'WAITING_CONFIRMATION':
            row['status'] = '<span class="bg-yellow-500 text-white rounded-full px-2 py-0.5 text-xs font-medium">Waiting</span>'
            row['actions'] = ''   

        elif obj.status == 'PROGRESS':
            row['status'] = '<span class="bg-orange-400 text-white rounded-full px-2 py-0.5 text-xs font-medium">On Progress</span>'
            row['actions'] = ''
            
        elif obj.status == 'CONFIRMED':
            row['status'] = '<span class="bg-green-600 text-white rounded-full px-2 py-0.5 text-xs font-medium">Confirmed</span>'
            row['actions'] = ''

        elif obj.status == 'DISCARDED':
            row['status'] = '<span class="bg-red-400 text-white rounded-full px-2 py-0.5 text-xs font-medium">Discarded</span>'
            row['actions'] = '' 

        elif obj.status == 'CLOSED':
            row['status'] = '<span class="bg-green-400 text-white rounded-full px-2 py-0.5 text-xs font-medium">Closed</span>'
            row['actions'] = ''

        else:
            row['status'] = row['status']
            row['actions'] = ''


class RumorList(AjaxDatatableView):
    model = Signal
    title = 'Rumors'
    show_column_filters = False
    initial_order = [["created_on", "desc"], ]
    length_menu = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'contents', 'title': 'Rumor', 'visible': True,
            'className': 'text-left flex-1 cursor-pointer'},
        #{'name': 'contents', 'title':'Contents','visible': True, 'className':' text-left'  },
        {'name': 'css_icon', 'title': '', 'visible': True,
            'className': 'w-6 text-left border-r', 'searchable': False, },
        {'name': 'relevance', 'title': '#', 'visible': True,
            'className': 'w-6 text-left border-r'},
        {'name': 'created_on', 'title': 'Received On', 'visible': True,
            'className': 'w-[120px] text-left border-r'},
        {'name': 'd', 'title': '', 'visible': True, 'className': 'w-6 text-left',
            'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        row['contents'] = '<span class=" line-clamp-1" @click="sidebarOpen = true, manageRumor('+str(
            obj.id)+')" >'+str(obj.contents['text'])+'</span>'
        row['css_icon'] = '<i class="'+obj.css_icon+'">'
        row['created_on'] = naturalday(obj.created_on)
        row['d'] = '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-500 hover:text-slate-600 hover:cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" @click="discardSignal('+str(
            obj.id)+')"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>'

    def get_initial_queryset(self, request=None):
        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method == 'GET' else request.POST

        queryset = self.model.objects.exclude(
            relevance=0).order_by('relevance')

        if 'status' in request.REQUEST:
            status = request.REQUEST.get('status')
            queryset = queryset.filter(status=status)

        return queryset
