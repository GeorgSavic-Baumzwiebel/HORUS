from django import template

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.simple_tag()
def update_variable(value):
    data = value
    return data


@register.filter
def divide(arg1, arg2):
    return arg1 / arg2

@register.filter
def mult(arg1, arg2):
    return arg1 * arg2

@register.filter
def return_item(l, i):
    try:
        return l[int(i)]
    except:
        return None