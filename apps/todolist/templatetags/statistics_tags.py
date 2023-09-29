from django import template
from apps.todolist.models import Task

register = template.Library()

@register.filter
def total_tasks(user):
    return Task.objects.filter(task_list__user=user).count()

@register.filter
def completed_tasks(user):
    return Task.objects.filter(task_list__user=user, done=True).count()