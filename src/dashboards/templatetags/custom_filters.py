from django import template
from vendors.models import Managers

register = template.Library()

@register.filter
def is_manager(user):
    return isinstance(user, Managers)
