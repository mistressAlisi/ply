from django import template
register = template.Library()
@register.filter(name='dict_str_key_or0int')
def dict_str_key_or0int(d, k):
    '''Returns the given key from a dictionary; casting the key as a string first.'''
    _k = str(k)
    if _k in d:
        return int(d[_k])
    else:
        return 0
