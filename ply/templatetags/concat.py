from django import template
register = template.Library()
@register.filter(name='concat')
def concat(a, b):
    '''Returns two strings concatenated together.'''
    return str(a)+str(b)
