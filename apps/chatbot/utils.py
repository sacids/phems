import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.chatbot.models import Menu, MenuLink, MenuSession, SubMenu


# call init menu
@csrf_exempt
def initMenu(channel, user):
    #get first menu
    menu = Menu.objects.get(flag='Menu_Tukio')

    #menu id
    menu_id = menu.id

    #create menu session
    createMenuSession(channel, user, menu_id)

    #process menu
    message = processMenu(menu_id)

    #response
    return JsonResponse({'status': 'success', 'message': message})


@csrf_exempt
def nextMenu(channel, user, menu_id, key):
    #update menu session
    updateMenuSession(channel, user, menu_id, key)

    #sub menu 
    sub_menu_key = SubMenu.objects.filter(menu_id=menu_id, sequence=key)

    if (sub_menu_key):
        #get menu link
        menu_link = MenuLink.objects.filter(menu_id=menu_id, sub_menu_id=sub_menu_key[0].id)

        if(menu_link):
            #create menu session
            createMenuSession(channel, user, menu_link[0].link_id)

            #process menu
            message = processMenu(menu_link[0].link_id)
        else:
            #todo: query last menu
            
            #message
            message = "No menu"     
    else: 
        #get menu link
        menu_link = MenuLink.objects.filter(menu_id=menu_id)

        if(menu_link):            
            #create menu session
            createMenuSession(channel, user, menu_link[0].link_id)

            #process menu
            message = processMenu(menu_link[0].link_id)
        else:
            #todo: query last menu

            #message
            message = "No menu"    

    return JsonResponse({'status': 'success', 'message': message})


@csrf_exempt
def processMenu(menu_id):
    #variables
    message = ''

    #get menu
    menu = Menu.objects.get(pk=menu_id)
    message = menu.title

    #get sub menu
    sub_menus = SubMenu.objects.filter(menu_id=menu_id).order_by('sequence')

    if(sub_menus):
        sub_message = ''
        for val in sub_menus:
            sub_message += val.sequence + "." + val.title + "\r\n"

        message = message + "\r\n" + sub_message;   

    #response
    return message

#create menu session
def createMenuSession(channel, user, menu_id):
    menu_session = MenuSession()
    menu_session.menu_id = menu_id
    menu_session.channel = channel

    #check for user => phone or message_id
    if(channel == 'whatsapp'):
        menu_session.phone = user
    elif(channel == 'telegram'):
        menu_session.message_id = user
    
    menu_session.save() 


#update menu session
def updateMenuSession(channel, user, menu_id, key):
    #check for user => phone or message_id
    if(channel == 'whatsapp'):
        MenuSession.objects.filter(channel=channel, phone=user, menu_id = menu_id).update(active=1, values=key)
    elif(channel == 'telegram'):
        MenuSession.objects.filter(channel=channel, message_id=user, menu_id = menu_id).update(active=1, values=key) 
    