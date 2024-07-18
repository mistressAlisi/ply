from django import template
register = template.Library()
@register.filter(name='fa_box_boolean')
def fa_box_boolean(bval):
    '''A font awesome checkbox icon: either A check or an Xmark for true or false, respectively.'''
    if bval is True:
        return '<i aria-hidden="true" title="Yes" class="fa-solid fa-square-check text-success"></i>'
    else:
        return '<i aria-hidden="true" title="No" class="fa-solid fa-square-xmark text-danger"></i>'
