from django import template
from django.conf import settings
from phonenumbers import format_number, PhoneNumberFormat


register = template.Library()


@register.filter('getattr')
def get_var_attr(obj, attr):
    return getattr(obj, attr, None)


@register.inclusion_tag('header.html')
def site_header(request):
    return {
        'request': request,
        'nav': {
            'Главная': 'index',
            'Все дома': 'homes',
            'Контакты': 'contacts'
        },
        'current_link': request.resolver_match.url_name,
        'org_phone_e164': format_number(settings.ORGANIZATION_MAIN_PHONE, PhoneNumberFormat.E164),
        'org_phone': format_number(settings.ORGANIZATION_MAIN_PHONE, PhoneNumberFormat.INTERNATIONAL)
    }


@register.inclusion_tag('footer.html')
def site_footer():
    return {
        'org_name': settings.ORGANIZATION_NAME,
    }
