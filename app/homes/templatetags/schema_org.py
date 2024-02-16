import json
from typing import TYPE_CHECKING, Any

from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from phonenumbers import format_number, PhoneNumberFormat

if TYPE_CHECKING:
    from homes.models import Home


register = template.Library()


@register.filter('so_organization')
def org_schema(homes: list["Home"]):
    return ld_json({
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": settings.ORGANIZATION_NAME,
        "url": reverse('index'),
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "RU",
            "addressRegion": "Краснодарский край",
            "addressLocality": "Краснодар",
        },
        "telephone": format_number(settings.ORGANIZATION_MAIN_PHONE, PhoneNumberFormat.E164),
        "openingHours": "Mo-Su",
        "hasOfferCatalog": homes_catalog_dict(homes)
    })


@register.filter('so_home')
def home_schema(home: "Home"):
    return ld_json({
        "@context": "https://schema.org",
        "@type": "Product",
        "name": home.name,
        "description": home.short_description,
        "image": home.cover.url,
        "offers": {
            "@type": "AggregateOffer",
            "lowPrice": home.cost_per_day,
            "priceCurrency": "руб/сутки"
        }
    })


@register.filter('so_homes_catalog')
def homes_catalog(homes: list["Home"]):
    return ld_json({
        "@context": "https://schema.org/",
        **homes_catalog_dict(homes)
    })


@register.filter('so_breadcrumbs')
def breadcrumbs(links: dict[str, str]):
    return ld_json({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": pos,
                "item": {"@id": str(url), "name": name}
            }
            for pos, (name, url) in enumerate(links.items(), start=1)
        ]
    })


def ld_json(data: dict[str, Any]):
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


def homes_catalog_dict(homes: list["Home"]):
    return {
        "@type": "OfferCatalog",
        "name": "Все коттеджи",
        "itemListElement": [
            {
                "@type": "Offer",
                "name": home.name,
                "description": home.short_description,
                "url": reverse('detail', args=[home.slug]),
                "price": home.cost_per_day,
                "priceCurrency": "руб/сутки",
                "image": home.cover.url,
            }
            for home in homes
        ]
    }
