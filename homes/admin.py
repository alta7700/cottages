from django.contrib import admin

from .models import Home, HomeCarouselImage, Ticket
from . import parsers
from .parsers import YaMapScriptParser, YTIframeParser


class CarouselInline(admin.StackedInline):
    model = HomeCarouselImage
    fields = ('position', 'image')
    max_num = 10
    extra = 0


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')

    list_editable = ('position',)

    fieldsets = (
        (
            None,
            {
                'fields': ('name', 'slug', 'address', 'position', 'cover', 'cost_per_day', 'show_on_site'),
            }
        ),
        (
            'Описание',
            {
                'classes': ['collapse'],
                'fields': ('short_description', 'long_description'),
            }
        ),
        (
            'Вставки',
            {
                'classes': ['collapse'],
                'fields': ('ya_map', 'video'),
            }
        ),
        (
            'Удобства',
            {
                'classes': ['collapse'],
                'fields': (
                    'conv_wifi', 'conv_minibar', 'conv_parking', 'conv_hairdryer',
                    'conv_workspace', 'conv_safe', 'conv_washing_machine', 'conv_swimming_pool',
                )
            }
        )
    )
    prepopulated_fields = {'slug': ('name', )}
    inlines = (CarouselInline, )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request=request, obj=obj, change=change, **kwargs)
        form.base_fields['ya_map'].validators.append(parsers.YaMapScriptParser.validate)
        form.base_fields['video'].validators.append(parsers.YTIframeParser.validate)
        return form

    def save_form(self, request, form, change):
        if 'ya_map' in form.changed_data:
            form.instance.ya_map = YaMapScriptParser.transform(form.cleaned_data['ya_map'])
        if 'video' in form.changed_data:
            form.instance.video = YTIframeParser.transform(form.cleaned_data['video'])
        return super().save_form(request=request, form=form, change=change)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('home', 'name', 'guest_count', 'start_date', 'status')
    fields = (
        'home', 'name', 'start_date', 'end_date', 'phone_number',
        'guest_count', 'created_at', 'status', 'comment'
    )
    readonly_fields = ('created_at',)
    list_filter = ('home', 'status')
    ordering = ('status', '-created_at')
    show_facets = admin.ShowFacets.ALWAYS

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
