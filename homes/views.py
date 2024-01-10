from django.views.generic import TemplateView

from .service import HomeService


class HomesIndexView(TemplateView):
    template_name = 'homes/index.html'

    extra_context = {'title': 'Аренда котеджей'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'homes': list(HomeService.get_available_homes_details()),
        })
        return context
