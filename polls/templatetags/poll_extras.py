from django import template

register = template.Library()

@register.filter(name='splitnumber')
def splitnumber(value:str):
    return '{:,}'.format(value)