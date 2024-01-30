from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from homes.models import Ticket


class TicketForm(forms.ModelForm):
    dtrange = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'readonly': True, 'placeholder': 'Выберите даты'}
    ))

    class Meta:
        model = Ticket
        fields = ('name', 'phone_number', 'guest_count', 'home')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'autocomplete': 'given-name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Номер телефона', 'autocomplete': 'phone'}),
            'guest_count': forms.NumberInput(attrs={'placeholder': 'Количество гостей'}),
        }

    def clean_dtrange(self):
        dtrange: str = self.cleaned_data['dtrange']
        start, _, end = dtrange.partition('-')
        if not start:
            raise ValidationError('Неверный формат')
        try:
            start = datetime.strptime(start.strip(), '%d.%m.%Y')
            end = start if not end else datetime.strptime(end.strip(), '%d.%m.%Y')
        except ValueError:
            raise ValidationError('Неверный формат')
        self.cleaned_data['start_date'] = start
        self.cleaned_data['end_date'] = end
        return dtrange

    def clean_name(self):
        name: str = self.cleaned_data['name']
        if not name:
            raise ValidationError('Не должно быть пустым')
        return name
