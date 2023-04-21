from ajax_datatable.views import AjaxDatatableView
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturalday
from .models import Event, Signal, Alert
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
        {'name': 'username', 'visible': 'Username', 'className': 'w-20 text-left border-r'},
        {'name': 'level','title': 'User Level' ,'foreign_field': 'profile__level', 'className': 'w-32 text-left border-r'},
        {'name': 'region','title': 'Region' ,'foreign_field': 'profile__region__title', 'className': 'w-32 text-left border-r'},
        {'name': 'roles', 'title': 'Roles','className': 'w-28 text-left border-r', 'searchable': False,},
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
            row['is_active'] = '<span class="bg-green-600 text-white px-2 py-0.5 text-xs font-normal rounded-full ">Active</span>' 
        elif obj.is_active == False:
            row['is_active'] = '<span class="bg-red-600 text-white px-2 py-0.5 text-xs font-normal rounded-full ">Inactive</span>'

        row['actions'] = '<div class="flex">'\
                '<a href="%s" class="btn btn-xss px-1">'\
                '<i class="bx bx-edit"></i>'\
                '</a>&nbsp;&nbsp;'\
                '<a href="%s" class="btn btn-xss">'\
                '<i class="bx bx-trash text-red-600"></i>' \
                '</a>'\
            '</div>' % (reverse('edit-user', args=(obj.id,)), reverse('delete-user', args=(obj.id,)))
        

class NotificationList(AjaxDatatableView):
    model = Notification
    title = 'Notifications'
    show_column_filters = False
    # initial_order = [["created_on", "desc"], ]
    length_menu = [[12, 50, 100, -1], [12, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'message', 'title': 'Message', 'visible': True, 'className': 'w-96 text-left border-r cursor-pointer'},
        {'name': 'created_on', 'title': 'Created On', 'visible': True,'className': 'w-8 text-left border-r'},
        {'name': 'status', 'title': 'Status', 'visible': True, 'className': 'w-8 text-left border-r'}
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        row['message'] = '<span class=" line-clamp-1" @click="sidebarOpen = true, manageNotification('+str(obj.id)+')" >' + str(obj.message) + '</span>'
        row['created_on'] = obj.created_on.strftime('%d/%m/%Y %H:%M')

        if obj.app_status == 'PENDING':
            row['status'] = '<span class="bg-amber-500 text-white rounded-lg px-2 py-0.5 text-xs font-normal">Pending</span>'
            
        elif obj.app_status == 'DELIVERED':
            row['status'] = '<span class="bg-green-600 text-white text-sm rounded-lg px-2 py-0.5 text-xs font-normal">Viewed</span>'  

        elif obj.app_status == 'REJECTED':
            row['status'] = '<span class="bg-red-500 text-white text-sm rounded-lg px-2 py-0.5 text-xs font-normal">Rejected</span>'

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
        {'name': 'title', 'visible': True, 'className': 'text-left w-max border-r'},
        {'name': 'region', 'foreign_field': 'region__title', 'visible': True,
            'max_length': 15, 'className': 'w-24 text-left border-r'},

        {'name': 'district', 'foreign_field': 'district__title', 'visible': True,
            'max_length': 15, 'className': 'w-28 text-left border-r'},

        {'name': 'alert', 'title': 'Alert Type', 'foreign_field': 'alert__label',
            'visible': True, 'className': 'w-36 text-left border-r'},

        {'name': 'pri_sector', 'foreign_field': 'pri_sector__title',
            'title': 'Primary Sector', 'visible': True, 'className': 'w-28 text-left border-r'},

        {'name': 'stage', 'visible': True, 'className': 'text-left whitespace-nowrap w-20 border-r'},

        {'name': 'created_on', 'title': 'Created', 'visible': True,
            'className': 'w-[100px] text-left border-r'},

        {'name': 'actions', 'title': '', 'visible': True, 'className': 'w-10 text-left border-r',
            'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        row['title']        = '<a class="hover:text-blue-600" href="%s">%s</a>' % (reverse('show-event', args=(obj.id,)), obj.title)
        row['created_on']   = naturalday(obj.created_on)
        row['stage']        = '<span class="text-white rounded-full px-2 py-0.5 text-xs font-normal ' + obj.stage.css + '">' + obj.stage.title + '</span>'
        
        if obj.stage.title == 'New':
            row['actions'] = '<div class="flex">'\
                '<a href="%s" class="btn btn-xss px-1">'\
                '<i class="bx bxs-folder-open text-blue-600"></i>'\
                '</a>&nbsp;&nbsp;'\
                '<a href="%s" class="btn btn-xss px-1">'\
                '<i class="bx bx-edit text-gray-600"></i>'\
                '</a>&nbsp;&nbsp;'\
                '<a href="%s" class="btn btn-xss">'\
                '<i class="bx bx-trash text-red-600"></i>' \
                '</a>'\
            '</div>' % (reverse('show-event', args=(obj.id,)) ,reverse('edit-event', args=(obj.id,)), reverse('delete-event', args=(obj.id,)))
        else:
            row['actions'] = '<div class="flex">'\
                    '<a href="%s" class="btn btn-xss px-1">'\
                    '<i class="bx bxs-folder-open text-blue-600"></i>'\
                    '</a>&nbsp;&nbsp;'\
                '</div>' % (reverse('show-event', args=(obj.id,)))


    def get_initial_queryset(self, request=None):
        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method == 'GET' else request.POST

        queryset = self.model.objects

        if self.request.user.profile.level == 'NATIONAL':
            queryset = queryset.all().order_by('-pk')

        elif self.request.user.profile.level == 'REGION': 
            queryset = queryset.filter(region_id=self.request.user.profile.region_id).order_by('-pk')

        elif self.request.user.profile.level == 'DISTRICT': 
            queryset = queryset.filter(district_id=self.request.user.profile.district_id).order_by('-pk')

        return queryset


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
        {'name': 'contents', 'title': 'Rumor', 'visible': True, 'className': 'text-left flex-1 cursor-pointer'},
        {'name': 'css_icon', 'title': '', 'visible': True, 'className': 'w-6 text-left border-r', 'searchable': False, },
        {'name': 'relevance', 'title': '#', 'visible': True, 'className': 'w-6 text-left border-r'},
        {'name': 'created_on', 'title': 'Received On', 'visible': True, 'className': 'w-[120px] text-left border-r'},
        {'name': 'actions', 'title': '', 'visible': True, 'className': 'w-6 text-left', 'placeholder': 'True', 'searchable': False, },
    ]

    def get_show_column_filters(self, request):
        return False

    def customize_row(self, row, obj):
        row['contents'] = '<span class=" line-clamp-1" @click="sidebarOpen = true, manageRumor('+str(obj.id)+')" >' + str(obj.contents['text']) + '</span>'
        row['css_icon'] = '<i class="'+obj.css_icon+'">'
        row['created_on'] = naturalday(obj.created_on)

        row['actions'] = '<a class="btn btn-xss" @click="discardSignal('+str(obj.id)+')">'\
                '<i class="bx bx-trash text-red-600"></i>' \
                '</a>'

    def get_initial_queryset(self, request=None):
        # We accept either GET or POST
        if not getattr(request, 'REQUEST', None):
            request.REQUEST = request.GET if request.method == 'GET' else request.POST

        queryset = self.model.objects.exclude(relevance=0).order_by('relevance')

        if 'status' in request.REQUEST:
            status = request.REQUEST.get('status')
            queryset = queryset.filter(status=status)

        return queryset
    

class AlertTypeList(AjaxDatatableView):
    model = Alert
    show_column_filters = False
    length_menu = [[16, 50, 100, -1], [16, 50, 100, 'all']]
    search_values_separator = '+'
    full_row_select = False

    column_defs = [
        {'name': 'id', 'visible': False, },
        {'name': 'reference', 'title': 'Reference', 'visible': True, 'className': 'text-left w-12 border-r'},
        {'name': 'label', 'title': 'Label', 'visible': True, 'className': 'w-36 text-left border-r', 'searchable': False, },
        {'name': 'title', 'title': 'Title', 'visible': True, 'className': 'w-96 text-left border-r'},
    ]
    def get_show_column_filters(self, request):
        return False
