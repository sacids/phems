from django.contrib import admin

from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *

# Register your models here.


class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_id','msisdn','current_tree','error_count','data','updated_on','active']

admin.site.register(Session, SessionAdmin)

admin.site.register(Node)

class MenuAdmin(admin.ModelAdmin):
    list_display = ['code','init_tree','output_url','test_numbers','active']
    
admin.site.register(Menu, MenuAdmin)
    
class NodeConfigInline(admin.StackedInline):
    model       = Node
    fk_name     = "tree"
    extra       = 1
    
class TreeAdmin(admin.ModelAdmin):
    list_display = ['title','show_text','argument','var_name','validation']
    inlines =[NodeConfigInline]

admin.site.register(Tree,TreeAdmin)