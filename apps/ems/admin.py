from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


from .models import *


class SignalAdmin(admin.ModelAdmin):
    list_display = ['id','channel','contents','relevance','status','created_on']
    
admin.site.register(Signal,SignalAdmin)


class SignalKeyAdmin(admin.ModelAdmin):
    list_display = ['keyword','weight']
    
admin.site.register(SignalKeys,SignalKeyAdmin)


class LocationAdmin(TreeAdmin):
    form = movenodeform_factory(Location)

admin.site.register(Location, LocationAdmin)


admin.site.register(Event)
admin.site.register(Stage)
admin.site.register(Contact)
admin.site.register(Sector)
admin.site.register(note)
admin.site.register(Form)
admin.site.register(Form_config)
admin.site.register(workflow_data)
admin.site.register(workflow_config)
