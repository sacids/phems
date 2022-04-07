from csv import list_dialects
from django.contrib import admin
from .models import Menu, MenuLink, SubMenu

# Register your models here.
class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'flag']
    search_fields = ['title__startwith']
    ordering = ("id",)
    inlines  = [SubMenuInline]


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu', 'sub_menu', 'link']
    ordering = ("id",)