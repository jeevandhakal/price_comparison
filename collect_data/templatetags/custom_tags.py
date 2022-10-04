import json
from django import template

register = template.Library()

@register.filter
def dict_to_str(value):
    return json.dumps(value)