from django import template

register = template.Library()

@register.filter
def task_status(task):
    if task.done:
        return "Done"
    else:
        return "Not Done"