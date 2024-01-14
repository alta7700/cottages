from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.http.response import HttpResponse, JsonResponse

from .forms import TicketForm
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

    ticket_form = TicketForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'homes': list(HomeService.get_available_homes_details()),
            'ticket_form': self.ticket_form,
        })
        return context


class CreateTicketView(FormMixin, View):
    form_class = TicketForm

    def post(self, request):
        form: TicketForm = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.start_date = form.cleaned_data['start_date']
            instance.end_date = form.cleaned_data['end_date']
            instance.save()
            return HttpResponse("OK", status=200)
        else:
            return JsonResponse({"errors": list(form.errors.keys())}, status=400)
