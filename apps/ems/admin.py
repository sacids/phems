from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *


class permsUserInline(GenericTabularInline):
    model = perms_user
    extra = 0

class SignalAdmin(admin.ModelAdmin):
    list_display = ['id','channel','contents','relevance','status','created_on']
    
admin.site.register(Signal,SignalAdmin)


class SignalKeyAdmin(admin.ModelAdmin):
    list_display = ['keyword','weight']
    
admin.site.register(SignalKeys,SignalKeyAdmin)


class LocationAdmin(TreeAdmin):
    form = movenodeform_factory(Location)

admin.site.register(Location, LocationAdmin)


class Form_configAdmin(admin.ModelAdmin):
    list_display = ['form','col_name' ,'col_type','constraints','page' ,'order' ]
    list_filter = ['form']

admin.site.register(Form_config,Form_configAdmin)


class AlertAdmin(admin.ModelAdmin):
    list_display = ['reference','label','title']

admin.site.register(Alert,AlertAdmin)


class FormConfigInline(admin.StackedInline):
    model = Form_config
    extra = 1
    
class FormAdmin(admin.ModelAdmin):
    inlines =[FormConfigInline]

    
admin.site.register(Form,FormAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['title','alert','stage','location','contact_phone','created_on']
    inlines =[permsUserInline]
    
admin.site.register(Event, EventAdmin)



class WorkflowConfigAdmin(admin.ModelAdmin):
    list_display    = ['label','wf_group','cur_stage','next_stage']
    list_filter     = ['wf_group']
    
    

class StageAdmin(admin.ModelAdmin):
    list_display    = ['id','title','css','form']
    list_editable   = ['title','css','form']
    

class NoteAdmin(admin.ModelAdmin):
    list_display    = ['id','message','content_type','created_by','created_at']
    

class FilesAdmin(admin.ModelAdmin):
    list_display    = ['id','title','obj','content_type','created_by','created_at']


admin.site.register(Stage, StageAdmin)
admin.site.register(Contact)
admin.site.register(Sector)
admin.site.register(note, NoteAdmin)
admin.site.register(files, FilesAdmin)
admin.site.register(workflow_data)
admin.site.register(workflow_config, WorkflowConfigAdmin)
admin.site.register(sitrep_config)
