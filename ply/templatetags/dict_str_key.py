from django import template
register = template.Library()
@register.filter(name='dict_str_key')
def dict_str_key(d, k):
    '''Returns the given key from a dictionary; casting the key as a string first.'''
    _k = str(k)
    if _k in d:
        return d[_k]
    else:
        return ""
