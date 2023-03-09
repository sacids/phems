from django import template


register = template.Library()

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


# @register.filter
# def show_task_notification(user_id):
#     tasks = Task.objects.filter(user_id=user_id, status='NEW')

#     if tasks.count() > 0:
#         return tasks.count()
#     else:
#         return ''
    
    

@register.simple_tag
def define(val=None):
  return val