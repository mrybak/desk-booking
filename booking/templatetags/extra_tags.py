__author__ = 'mrybak'

from django import template

register = template.Library()

def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

register.filter('mult', mult)
