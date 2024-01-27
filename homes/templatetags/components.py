from typing import Literal, TYPE_CHECKING

from django import template

if TYPE_CHECKING:
    from homes.models import Home

register = template.Library()


@register.inclusion_tag('components/button.html')
def button(
        text: str = None,
        size: Literal['m', 'l'] = 'm',
        color: Literal['dark', 'light'] = 'dark',
        icon: str = None,
        leading_icon: str = None,
        trailing_icon: str = None,
        extra_classes: str = None,
        type: str = 'button',
        id: str = None,
):
    leading_icon = leading_icon or icon
    assert text or leading_icon
    return {
        'text': text,
        'color': color,
        'size': {'m': 'medium', 'l': 'large'}[size],
        'leading_icon': f'svg/{leading_icon}.html' if leading_icon else None,
        'trailing_icon': f'svg/{trailing_icon}.html' if trailing_icon else None,
        'icon_button': not text,
        'extra_classes': extra_classes,
        'type': type,
        'id': id,
    }


@register.inclusion_tag('components/conveniences.html')
def conveniences(home: "Home", add_text: bool = True):
    return {
        'conveniences': {conv_icons[conv]: text for conv, text in home.conveniences.items()},
        'add_text': add_text
    }


conv_icons = {
    'wifi': 'svg/wifi.html',
    'minibar': 'svg/coctail.html',
    'parking': 'svg/parking.html',
    'hairdryer': 'svg/hairdryer.html',
    'workspace': 'svg/business.html',
    'safe': 'svg/locker.html',
    'washing_machine': 'svg/washing_machine.html',
    'swimming_pool': 'svg/pool.html',
}
