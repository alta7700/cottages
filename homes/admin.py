from django.contrib import admin

from .models import Home, HomeCarouselImage


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
                    'has_wifi', 'has_minibar', 'has_parking', 'has_fan', 'has_workspace',
                    'has_safe', 'has_washing_machine', 'has_swimming_pool',
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
