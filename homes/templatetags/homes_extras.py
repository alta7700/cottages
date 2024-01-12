from django import template


register = template.Library()


@register.filter('getattr')
def get_var_attr(obj, attr):
    return getattr(obj, attr, None)
