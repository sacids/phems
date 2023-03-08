from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from django.views import generic
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.humanize.templatetags.humanize import naturalday
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import EventForm

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

class EventListView2(generic.ListView):
    model = Event
    context_object_name = 'events'
    template_name = "events/list.html"


class EventList2View(generic.TemplateView):
    template_name = "ems/events.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        return super(EventList2View, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(EventList2View, self).get_context_data(**kwargs)
        context['signals'] = Signal.objects.filter(status='NEW')
        context['events'] = Event.objects.all().order_by('-pk')
        context['sectors'] = Sector.objects.all()
        context['workflows'] = workflow_config.objects.all()
        context['profession'] = Event.PROFESSION
        context['alerts'] = Alert.objects.all().order_by('reference')

        return context


class EventListView(generic.TemplateView):
    template_name = "events/lists.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all().order_by('-pk')
        context['sectors'] = Sector.objects.all()
        context['workflows'] = workflow_config.objects.all()
        context['profession'] = Event.PROFESSION
        context['alerts'] = Alert.objects.all().order_by('reference')
        return context


class EventDetailView(generic.TemplateView):
    template_name = "events/details.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        context = super(EventView, self).get_context_data(**kwargs)
        
        eid                     = self.kwargs['eid']
        event_obj               = Event.objects.get(pk=eid)
        context['event']        = event_obj
        context['workflows']    = workflow_config.objects.all()
        context['alerts']       = Alert.objects.filter(event__id=eid)
        context['e_col_u']      = event_obj.user_access.all()
        
        ''' 
        user_perms              = event_obj.user_access.all()
        plist                   = []
        for perm in user_perms:
            plist.append(perm.user.id)
        context['user_perms']   = plist
        context['users']        = User.objects.all()

        group_perms               = event_obj.group_access.all()
        plist                   = []
        for perm in group_perms:
            plist.append(perm.group.id)
        context['group_perms']   = plist
        context['groups']        = Group.objects.all()
        '''
        return context


class EventCreateView(generic.CreateView):
    """Create new event"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.all()

        context = {'form': EventForm(), 'sectors': sectors}
        return render(request, 'events/create.html', context)

    def post(self, request, *args, **kwargs):
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.created_by = self.request.user
            new_event.save()

            # """insert sector"""
            # sector_ids = request.POST.getlist('sector_ids')

            # for sector_id in sector_ids:
            #     new_event.sector.add(sector_id)

            """message"""
            messages.success(request, 'New event created!')

            """redirect"""
            return HttpResponseRedirect(reverse_lazy('events'))
        return render(request, 'events/create.html', {'form': form})


class EventUpdateView(generic.UpdateView):
    """View to update"""
    model = Event
    context_object_name = 'event'
    form_class = EventForm
    template_name = 'events/edit.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.updated_by = self.request.user
        response.save()

        """message"""
        messages.success(self.request, 'Event Updated!')

        """redirect to events"""
        return HttpResponseRedirect(reverse_lazy('events'))


def event_activities(request, **kwargs):
    """event activities"""
    event = Event.objects.get(pk=kwargs['pk'])

    """activities"""
    activities = Activity.objects.filter(event_id= event.id).order_by('created_on')

    """context"""
    context = {
        'event': event,
        'activities': activities
    }

    """render view"""
    return render(request, 'events/async/activities.html', context=context)


def initiate_event(request, **kwargs):
    """Initiate event"""
    event = Event.objects.get(pk=kwargs['pk'])

    """sectors"""
    sectors = Sector.objects.all()

    """context"""
    context = {
        'event': event,
        'sectors': sectors
    }

    """render view"""
    return render(request, 'events/async/initiate.html', context=context)


def request_event_confirmation(request):
    """request for confirmation"""
    if request.method == 'POST':
        ev_id = request.POST.get("event_id")
        action = request.POST.get("action")

        """event"""
        event = Event.objects.get(pk=ev_id)

        """ update event status to WAITING_APPROVAL """
        event.status = "WAITING_APPROVAL"
        event.save()

        """create or update activities logs based on event and action"""
        activity, created = Activity.objects.update_or_create(event_id=ev_id, action=request.POST.get("action"), defaults={"remarks": request.POST.get("remarks"), "created_by": request.user})

        """upload attachment attachment"""
        if request.FILES['attachment']:
            new_attachment = ActivityAttachment()
            new_attachment.activity_id = activity.id
            new_attachment.attachment = request.FILES['attachment']
            new_attachment.save()

        """attach event to sectors"""
        sector_ids = request.POST.getlist('sector_ids')

        for sector_id in sector_ids:
            event.sector.add(sector_id)

        """TODO: send notification tagged sectors"""

        """response"""
        response = 'Successfully requested confirmation to sectors.'
    else:
        response = "Failed to request confirmation to sectors."

    """return response"""
    return JsonResponse(response, safe=False)


def confirm_event(request, **kwargs):
    """Confirm event"""
    event = Event.objects.get(pk=kwargs['pk'])

    """context"""
    context = {
        'event': event,
    }

    """render view"""
    return render(request, 'events/async/confirm.html', context=context)


def update_event_confirmation(request):
    """updated event confirmation"""
    if request.method == 'POST':
        ev_id = request.POST.get("event_id")
        action = request.POST.get("action")

        """event"""
        event = Event.objects.get(pk=ev_id)

        """update event status"""
        event.status = "CONFIRMED"
        event.save()

        """create or update activities logs based on event and action"""
        activity, created = Activity.objects.update_or_create(event_id=ev_id, action=request.POST.get("action"), defaults={"remarks": request.POST.get("remarks"), "created_by": request.user})

        """upload attachment attachment"""
        if request.FILES['attachment']:
            new_attachment = ActivityAttachment()
            new_attachment.activity_id = activity.id
            new_attachment.attachment = request.FILES['attachment']
            new_attachment.save()


        """TODO: send notification tagged sectors"""

        """response"""
        response = 'Alert confirmed.'
    else:
        response = "Failed to confirm alert."

    """return response"""
    return JsonResponse(response, safe=False)


def report_event_progress(request, **kwargs):
    """Initiate event"""
    event = Event.objects.get(pk=kwargs['pk'])

    """context"""
    context = {
        'event': event,
    }

    """render view"""
    return render(request, 'events/async/report_progress.html', context=context)


def update_report_progress(request):
    """updated report progress"""
    if request.method == 'POST':
        ev_id = request.POST.get("event_id")
        action = request.POST.get("action")

        """event"""
        event = Event.objects.get(pk=ev_id)

        """update event status"""
        event.status = "PROGRESS"
        event.save()

        """create or update activities logs based on event and action"""
        activity = Activity()
        activity.event_id = event.id
        activity.remarks = request.POST.get("remarks")
        activity.action  = request.POST.get("action")
        activity.created_by = request.user
        activity.save()

        """upload attachment attachment"""
        if request.FILES['attachment']:
            new_attachment = ActivityAttachment()
            new_attachment.activity_id = activity.id
            new_attachment.attachment = request.FILES['attachment']
            new_attachment.save()


        """TODO: send notification tagged sectors"""

        """response"""
        response = 'Alert progress updated.'
    else:
        response = "Failed to update alert progress."

    """return response"""
    return JsonResponse(response, safe=False)


class SignalListView(generic.TemplateView):
    template_name = "ems/signals.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        return super(SignalListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super(SignalListView, self).get_context_data(**kwargs)
        context['signals'] = Signal.objects.filter(
            status='NEW').order_by('-created_on')
        context['profession'] = Event.PROFESSION
        context['sectors'] = Sector.objects.all()
        context['events'] = Event.objects.all()
        context['alerts'] = Alert.objects.all()
        context['t_doy'] = date.today().timetuple().tm_yday
        context['w_doy'] = date.today().timetuple().tm_yday - 7
        return context


class RumorListView(generic.TemplateView):
    template_name = "rumors/lists.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RumorListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RumorListView, self).get_context_data(**kwargs)
        context['profession'] = Event.PROFESSION
        context['sectors'] = Sector.objects.all()
        context['events'] = Event.objects.all()
        context['alerts'] = Alert.objects.all()
        context['t_doy'] = date.today().timetuple().tm_yday
        context['w_doy'] = date.today().timetuple().tm_yday - 7
        return context


def listing_events(request):
    """list all alerts"""
    events = Event.objects.all().order_by('-pk')

    arr_data = []
    for val in events:
        event = {
            'id': val.id,
            'title': val.title,
            'description': val.description,
            'location': val.location.title,
            'status': val.status,
            'created_on': val.created_on
        }
        arr_data.append(event)

    return JsonResponse(arr_data, safe=False)


def delete_signal(request):
    """change rumor status to DISCARDED"""
    sig_id = request.GET.get('sid', 0)
    sig_obj = Signal.objects.get(pk=sig_id)
    sig_obj.status = 'DISCARDED'
    sig_obj.save()

    """return response"""
    return JsonResponse({"error": False, "success_msg": "Rumor discarded"}, safe=False)


def delete_item(request):
    """delete item"""
    item_id = request.GET.get('ii', 0)
    item_ty = request.GET.get('it', 0)

    if item_ty == 'si':
        sig_obj = Signal.objects.get(pk=item_id)
        sig_obj.status = 'DISCARDED'
        sig_obj.save()

    if item_ty == 'ev':
        sig_obj = Event.objects.get(pk=item_id)
        sig_obj.status = 'DISCARDED'
        sig_obj.save()

    """return response"""
    return JsonResponse(1, safe=False)


def manage_rumor(request):
    sig_id = request.GET.get('sid', 0)

    context = {}
    context['signal'] = Signal.objects.get(pk=sig_id)
    context['sig_id'] = sig_id
    context['events'] = Event.objects.all()
    context['sectors'] = Sector.objects.all()
    context['profession'] = Event.PROFESSION
    context['alerts'] = Alert.objects.all()

    template = 'rumors/async/manage_signal.html'
    return TemplateResponse(request, template, context)


def promote_signal(request):

    sig_id = request.GET.get('sid', 0)

    context = {}
    context['signal'] = Signal.objects.get(pk=sig_id)
    context['events'] = Event.objects.all()
    context['sectors'] = Sector.objects.all()
    context['profession'] = Event.PROFESSION

    template = 'events/async/promote_signal.html'

    return TemplateResponse(request, template, context)


def add_event(request):
    """create new event from the signal"""
    if request.method == 'POST':
        """new event"""
        new_event = Event()
        new_event.title = request.POST.get('title')
        new_event.description = request.POST.get('description')
        new_event.alert_id = request.POST.get('alert_id')
        new_event.location_id = request.POST.get('location_id')
        new_event.pri_sector_id = request.POST.get('pri_sector_id')
        new_event.save()

        # """insert sector"""
        # sector_ids = request.POST.getlist('sector_ids')

        # for sector_id in sector_ids:
        #     new_event.sector.add(sector_id)

        """signal"""
        signal = Signal.objects.get(pk=request.POST.get('signal'))

        """attach signal to new event """
        new_event.signal.add(signal.id)

        """change status of signal"""
        signal.status = "ADDED"
        signal.save()

        """TODO: send notification to manager to attach sector ministries to act"""

        """response"""
        response = 'New alert created'

    else:
        response = "Failed to create alert!"

    """return response"""
    return JsonResponse(response, safe=False)


def SitrepForm(request, *args, **kwargs):
    
    form_id                 = kwargs.get('form_id')
    alert_id                = kwargs.get('alert_id')
    
    context                 = {}
    context['multiple']     = sitrep_config.objects.filter(form_id=form_id)[0].multiple
    context['form_details'] = Form_config.objects.filter(form_id=form_id)
    context['alert_id']     = alert_id
    
    #fc = Form_config.objects.filter(form_id=form_id)
    #for a in fc:
    #    print(a.form.sitrep_form.get().multiple)
    
    def attach_sig2event(request):
    """attach rumor to alert"""
    sig_id              = request.GET.get('sid',0) 
    evt_id              = request.GET.get('eid',0)

    print("reached here")
    
    """query for event and signal"""
    event = Event.objects.get(pk=evt_id)
    signal = Signal.objects.get(pk=sig_id)
    event.signal.add(signal)

    """change status of rumor"""
    signal.status = 'ADDED'
    signal.save()

    """TODO: send notification to manager to attach sector ministries to act"""

    """response"""
    response = 'New alert created'

    """return response"""
    return JsonResponse(1, safe=False)


def get_event_data(request):

    eid = request.GET.get('eid', 0)
    data = _get_event_data(eid)

    return JsonResponse(data, safe=False)


def _get_event_data(eid):

    all_data = workflow_data.objects.filter(
        event__id=eid).order_by('-created_at')
    data = []

    for n in all_data:

        tmp = {}
        tmp['stage'] = n.stage.title
        tmp['created_at'] = naturalday(n.created_at)
        tmp['name'] = n.created_by.first_name+' '+n.created_by.last_name

        y = json.loads(n.data)
        tmp2 = {}
        for k, v in y.items():
            tmp2[k] = v

        tmp['data'] = tmp2
        data.append(tmp)

        return data


def get_colabs(request):
    eid = request.GET.get('eid', 0)
    event_obj = Event.objects.get(pk=eid)
    all_colabs = event_obj.user_access.all()
    colabs = []

    for n in all_colabs:
        tmp = {
            "id":           n.user.id,
            "initials":     n.user.first_name[0].upper()+n.user.last_name[0].upper(),
            "name":         n.user.first_name+' '+n.user.last_name,
            "email":        n.user.email,
        }

        colabs.append(tmp)
    return JsonResponse(colabs, safe=False)


def add_colabs(request):

    usr_id = request.POST.get('uid', 0)
    evt_id = request.POST.get('eid', 0)

    evt_obj = Event.objects.get(pk=evt_id)
    usr_obj = User.objects.get(pk=usr_id)

    # obj.user_access.create(user=sel_user)

    evt_obj.user_access.create(user=usr_obj)

    # ADD COMMENT
    note = request.user.first_name + ' added ' + \
        usr_obj.first_name+' as collaborator '
    evt_obj.notes.create(message=note, created_by=User.objects.get(pk=1))

    tmp = {
        "id":           usr_obj.id,
        "initials":     usr_obj.first_name[0].upper()+usr_obj.last_name[0].upper(),
        "name":         usr_obj.first_name+' '+usr_obj.last_name,
        "email":        usr_obj.email,
    }

    return JsonResponse(tmp, safe=False)


def del_colabs(request):

    usr_id = request.POST.get('uid', 0)
    evt_id = request.POST.get('eid', 0)

    evt_obj = Event.objects.get(pk=evt_id)
    usr_obj = User.objects.get(pk=usr_id)

    evt_obj.user_access.filter(user=usr_obj).delete()

    # ADD COMMENT
    note = request.user.first_name + ' removed ' + \
        usr_obj.first_name+' as collaborator '
    evt_obj.notes.create(message=note, created_by=User.objects.get(pk=1))

    return JsonResponse(1, safe=False)


def get_notes(request):

    eid = request.GET.get('eid', 0)
    notes = _get_event_notes(eid)

    return JsonResponse(notes, safe=False)


def _get_event_notes(eid):
    event_obj = Event.objects.get(pk=eid)
    all_notes = event_obj.notes.all().order_by('-created_at')
    notes = []

    for n in all_notes:
        tmp = {
            "message":      n.message,
            "initials":     n.created_by.first_name[0].upper()+n.created_by.last_name[0].upper(),
            "name":         n.created_by.first_name+' '+n.created_by.last_name,
            "created_on":   naturalday(n.created_at),
        }

        notes.append(tmp)
    return notes


def get_files(request):

    eid = request.GET.get('eid', 0)
    files = _get_event_files(eid)
    return JsonResponse(files, safe=False)


def _get_event_files(eid):
    event_obj = Event.objects.get(pk=eid)
    all_files = event_obj.files.all().order_by('-created_at')
    files = []

    for n in all_files:
        tmp = {
            "css_icon":      n.css_icon,
            "file_name":     n.filename,
            "created_on":    naturalday(n.created_at),
            "url":           n.obj.url,
        }

        files.append(tmp)

    return files


def manage_event(request):

    eid = request.GET.get('eid', 0)
    Event_obj = Event.objects.get(pk=eid)
    context = {}

    context['event'] = Event_obj
    context['notes'] = Event_obj.notes.all()

    template = 'events/async/manage_event.html'

    return TemplateResponse(request, template, context)

def attach_sig2event(request):
    
    sig_id              = request.GET.get('sid',0) 
    evt_id              = request.GET.get('eid',0)
    
    event   = Event.objects.get(pk=evt_id)
    signal  = Signal.objects.get(pk=sig_id)
    event.signal.add(signal)
    
    # if attache success
    signal.status = 'ADDED'
    signal.save()
    
    return JsonResponse(1,safe=False)


def upload_file(request):

    if request.method == 'POST' and request.FILES['obj']:
        event = Event.objects.get(pk=request.POST.get('event_id'))
        event.files.create(
            obj=request.FILES['obj'], title='sample title', created_by=request.user)

    return JsonResponse(1, safe=False)


def add_note(request):

    if request.method == 'POST':
        event = Event.objects.get(pk=request.POST.get('event_id'))
        event.notes.create(message=request.POST.get(
            'message'), created_by=request.user)

    return JsonResponse(1, safe=False)


def search_location(request):

    term = request.GET.get('term', 0)
    node = Location.objects.filter(title__icontains=term)

    data = []
    for item in node:
        par = item.get_parent()

        tmp = {}
        tmp['id'] = item.id
        text = par.title+' - '+item.title
        tmp['text'] = (text.replace("'", "")).lower().title()
        data.append(tmp)

    results = {}
    results['results'] = data

    return JsonResponse(results, safe=False)


def search_users(request):

    term = request.GET.get('term', 0)
    user_qs = User.objects.filter(
        Q(first_name__icontains=term) |
        Q(last_name__icontains=term) |
        Q(email__icontains=term) |
        Q(username__icontains=term))

    data = []
    for item in user_qs:

        tmp = {}
        tmp['id'] = item.id
        text = item.first_name+' '+item.last_name
        tmp['text'] = (text.replace("'", "")).lower().title()
        data.append(tmp)

    results = {}
    results['results'] = data

    return JsonResponse(results, safe=False)


def get_list(list_name):
    with open("assets/json/location/"+list_name+".json", 'r') as file:
        regions = json.loads(file.read().rstrip())
    return JsonResponse(1, safe=False)


def change_wf(request):
    new_stage = request.GET.get('ns')
    event_id = request.GET.get('ei')
    form_id = request.GET.get('fi')

    context = {}
    context['new_stage'] = new_stage
    context['event_id'] = event_id
    context['form_details'] = Form_config.objects.filter(form_id=form_id)

    # for i in context['form_details']:
    #    print(i)

    return TemplateResponse(request, "ems/async/form_detail.html", context=context)


def get_alert_data(request):

    draw = request.GET.get('draw')
    row = request.GET.get('start')
    rowperpage = request.GET.get('length')
    columnIndex = request.GET.get('order')
    columnName = request.GET.get('columns')
    columnSortOrder = request.GET.get('order')
    searchValue = request.GET.get('search')

    data = {
        "data": [
            {
                "id": "1",
                "name": "Tiger Nixon",
                "position": "System Architect",
                "salary": "$320,800",
                "start_date": "2011/04/25",
                "office": "Edinburgh",
                "extn": "5421"
            },
            {
                "id": "2",
                "name": "Garrett Winters",
                "position": "Accountant",
                "salary": "$170,750",
                "start_date": "2011/07/25",
                "office": "Tokyo",
                "extn": "8422"
            },
            {
                "id": "3",
                "name": "Ashton Cox",
                "position": "Junior Technical Author",
                "salary": "$86,000",
                "start_date": "2009/01/12",
                "office": "San Francisco",
                "extn": "1562"
            },
            {
                "id": "4",
                "name": "Cedric Kelly",
                "position": "Senior Javascript Developer",
                "salary": "$433,060",
                "start_date": "2012/03/29",
                "office": "Edinburgh",
                "extn": "6224"
            },
            {
                "id": "5",
                "name": "Airi Satou",
                "position": "Accountant",
                "salary": "$162,700",
                "start_date": "2008/11/28",
                "office": "Tokyo",
                "extn": "5407"
            }
        ]
    }
    return JsonResponse(data, safe=False)


def update_wf(request):
    formData = request.POST.get('fda')
    event_id = request.POST.get('eid')
    next_stage = request.POST.get('nst')

    eventObj = Event.objects.get(pk=event_id)
    stageObj = Stage.objects.get(pk=next_stage)

    # UPDATE WORKFLOW
    wfObj = workflow_data()
    wfObj.event = eventObj
    wfObj.stage = stageObj
    wfObj.data = formData
    wfObj.created_by = request.user
    wfObj.save()

    # ADD COMMENT
    note = request.user.first_name + ' changed stage from ' + \
        eventObj.stage.title+' to '+stageObj.title
    eventObj.notes.create(message=note, created_by=request.user)

    # UPDATE OBJECT
    eventObj.stage = stageObj
    eventObj.save()

    return JsonResponse(1, safe=False)


def manage_event_act(request):

    event_id = request.GET.get('eid', '')
    event_act = request.GET.get('act', '')
    Event_obj = Event.objects.get(pk=event_id)

    context = {}

    if event_act == 'sa':
        # ALL
        context['event'] = Event_obj
        context['notes'] = Event_obj.notes.all()
        template = 'events/async/e_all.html'

    elif event_act == 'sn':
        # NOTES
        context['notes'] = Event_obj.notes.all()
        template = 'events/async/e_notes.html'

    elif event_act == 'ss':
        # SIGNALS
        context['signals'] = Event_obj.signal.all()
        template = 'events/async/e_signals.html'

    elif event_act == 'sf':
        # FILES
        context['files'] = Event_obj.files.all()
        template = 'events/async/e_files.html'

    else:
        # FILES
        context['files'] = Event_obj.files.all()
        template = 'events/async/e_files.html'

    return TemplateResponse(request, template, context)


"""
def build_location_db(request):

    root        = Location.objects.get(pk=1)
    regions     = get_list('regions')
    districts   = get_list('districts')
    wards       = get_list('wards')
    villages    = get_list('villages')

    for region in regions:
        r_node    = root.add_child(title=region['name'],code=region['code'],p_id='r_'+(str(region['id'])).strip())
    
    for district in districts:
        r_id      = 'r_'+str(district['region_id'])
        try:
            r_node    = Location.objects.get(p_id=r_id.strip())
            r_node.add_child(title=district['name'],code=soundex(district['name']),p_id='d_'+str(district['id']).strip())
        except Location.DoesNotExist:
            print('District '+r_id)

    for ward in wards:
        d_id      = 'd_'+str(ward['district_id'])
        try:
            d_node    = Location.objects.get(p_id=d_id.strip())
            w_node    = d_node.add_child(title=ward['name'],code=soundex(ward['name']),p_id='w_'+(str(ward['id'])).strip())
        except Location.DoesNotExist:
            print('Ward '+d_id)

    for village in villages:
        w_id      = 'w_'+str(village['ward_id'])
        try:
            w_node    = Location.objects.get(p_id=w_id.strip())
            v_node    = w_node.add_child(title=village['name'],code=soundex(village['name']),p_id='v_'+(str(village['id'])).strip())
        except Location.DoesNotExist:
            print('Village '+w_id)


    return HttpResponse('moja')
"""


@login_required
def submitPermsForm(request):

    template = 'mrv/ajax/lib_form_input.html'
    if request.method == 'POST':

        users = request.POST.getlist('u_access')
        groups = request.POST.getlist('g_access')
        eid = request.POST.get('eid')

        # reset perms to new values
        resetPerms(users, groups, eid)

        obj = Event.objects.get(pk=eid)

        context = {
            'library': obj,
        }
        user_perms = obj.user_access.all()
        plist = []
        for perm in user_perms:
            plist.append(perm.user.id)
        context['user_perms'] = plist
        context['users'] = User.objects.all()

        group_perms = obj.group_access.all()
        plist = []
        for perm in group_perms:
            plist.append(perm.group.id)
        context['group_perms'] = plist
        context['groups'] = Group.objects.all()

        template = 'mrv/ajax/lib_access.html'

        return TemplateResponse(request, template, context)
    else:
        return JsonResponse(0)


def resetPerms(users, groups, eid):
    obj = Event.objects.get(pk=eid)
    obj.user_access.all().delete()
    obj.group_access.all().delete()

    for id in users:
        sel_user = User.objects.get(pk=id)
        obj.user_access.create(user=sel_user)

    for id in groups:
        # perms_group.objects.create(content_object=obj,group=Group.objects.get(pk=id))
        sel_group = Group.objects.get(pk=id)
        obj.group_access.create(group=sel_group)
