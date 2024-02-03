from django import template
register = template.Library()
@register.filter(name='to_str')
def to_str(v):
    '''Returns v as a str. '''
    return str(v)
