from django.views.generic import TemplateView

from .service import HomeService


nav = {
    'Главная': 'homes:index',
    'Все дома': 'homes:homes',
    'Контакты': 'homes:contacts'
}


class HomesIndexView(TemplateView):
    template_name = 'homes/home_details.html'

    extra_context = {
        'title': 'Аренда котеджей в Краснодаре',
        'initial_active_home': 0,
        'current_link': 'homes:index',
        'nav': nav,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'homes': list(HomeService.get_available_homes_details()),
        })
        return context
