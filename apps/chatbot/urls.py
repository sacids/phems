from django.urls import path
from django.urls.resolvers import URLPattern
from . import views, utils

urlpatterns = [
    path("whatsapp/", views.whatsapp, name="whatsapp"),
    path("telegram/", views.telegram, name="telegram"),

    #utils
    # path("utils/init_menu/", utils.initMenu, name="initMenu"),
    # path("utils/next_menu/", utils.nextMenu, name="nextMenu"),
    # path("utils/process_menu/", utils.processMenu, name="processMenu"),
]