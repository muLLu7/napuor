from django import template
register = template.Library()

@register.filter 
def multiply(arg1, arg2): 
    return float(arg1) * float(arg2)