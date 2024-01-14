from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect

from .forms import TicketForm
from .service import HomeService


nav = {
    'Главная': 'homes:index',
    'Все дома': 'homes:homes',
    'Контакты': 'homes:contacts'
}


class BaseHomeDetailsView(TemplateView):
    extra_context = {
        'title': 'Аренда котеджей в Краснодаре',
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


class HomesIndexView(BaseHomeDetailsView):
    template_name = 'homes/index.html'


class HomeDetailsView(BaseHomeDetailsView):
    template_name = 'homes/home_details.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        for home in context['homes']:
            if home.slug == slug:
                context['initial_home'] = home
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'initial_home' not in context:
            return HttpResponseRedirect(reverse('homes:index'))
        return self.render_to_response(context)


class AllHomesView(TemplateView):
    template_name = 'homes/all_homes.html'
    extra_context = {
        'title': 'Аренда котеджей в Краснодаре',
        'current_link': 'homes:homes',
        'nav': nav,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'homes': list(HomeService.get_available_homes()),
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
