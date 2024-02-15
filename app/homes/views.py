from django.views.generic import TemplateView, View
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.conf import settings
from phonenumbers import format_number, PhoneNumberFormat

from .forms import TicketForm
from .service import HomeService


default_seo = {
    'title': settings.ORGANIZATION_NAME,
    'seo_description': 'Наши коттеджи - это не просто место для отдыха, '
                       'а пространство, где роскошь и комфорт становятся '
                       'вашими верными спутниками. Забронируйте уже сегодня '
                       'и подарите себе незабываемый опыт в самом центре Краснодара!',
    'seo_keywords': 'аренда, коттедж, краснодар',
    'og__site_name': f'{settings.ORGANIZATION_NAME}: Аренда коттеджей в Краснодаре',
}


class BaseHomeDetailsView(TemplateView):
    extra_context = {
        **default_seo,
        'title': f'{settings.ORGANIZATION_NAME}: Аренда коттеджей в Краснодаре',
        'topic': settings.ORGANIZATION_NAME,
        'og__title': 'Просмотр коттеджей',
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
    template_name = 'homes/details.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        for home in context['homes']:
            if home.slug == slug:
                context.update({
                    'initial_home': home,
                    'title': f'{settings.ORGANIZATION_NAME}: {home.name}',
                    'seo_description': home.short_description[:170] + '...',
                    'seo_keywords': f'{context['seo_keywords']}, {home.area}',
                    'og__title': 'Забронировать: ' + home.name,
                })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'initial_home' not in context:
            return HttpResponseRedirect(reverse('index'))
        return self.render_to_response(context)


class AllHomesView(TemplateView):
    template_name = 'homes/all_homes.html'
    extra_context = {
        **default_seo,
        'title': settings.ORGANIZATION_NAME + ": Все коттеджи",
        'og__title': "Все коттеджи",
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


class ContactsView(TemplateView):
    extra_context = {
        **default_seo,
        'title': settings.ORGANIZATION_NAME + ': Контакты',
        'seo_keywords': default_seo['seo_keywords'] + ', позвонить',
        'og__title': 'Контакты',
        'og__description': 'Позвоните или напишите, чтобы узнать больше о наших коттеджах и забронировать.',
        'map': mark_safe(settings.GENERAL_MAP),
        'phones': [{
            'e164': format_number(phone, PhoneNumberFormat.E164),
            'display': format_number(phone, PhoneNumberFormat.INTERNATIONAL),
        } for phone in settings.ORGANIZATION_PHONES],
        'instagram': settings.ORGANIZATION_INSTAGRAM,
        'mails': settings.ORGANIZATION_MAILS,
    }
    template_name = 'contacts.html'
