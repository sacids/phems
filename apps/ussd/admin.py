from django.contrib import admin

from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *

# Register your models here.


admin.site.register(Menu)
admin.site.register(Session)
admin.site.register(Node)


class NodeConfigInline(admin.StackedInline):
    model       = Node
    fk_name     = "tree"
    extra       = 1
    
class TreeAdmin(admin.ModelAdmin):
    inlines =[NodeConfigInline]

    
admin.site.register(Tree,TreeAdmin)