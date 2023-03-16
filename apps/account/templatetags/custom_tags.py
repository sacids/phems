from django import template
from apps.notification.models import Notification

register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def show_notification(user_id):
    tasks = Notification.objects.filter(user_id=user_id, app_status='PENDING')

    if tasks.count() > 0:
        return tasks.count()
    else:
        return 0
    
    

@register.simple_tag
def define(val=None):
  return val