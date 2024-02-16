from django.urls import path

from . import views


urlpatterns = [
    path('homes', views.AllHomesView.as_view(), name='homes'),
    path('homes/<slug:slug>', views.HomeDetailsView.as_view(), name='detail'),
    path('contacts', views.ContactsView.as_view(), name='contacts'),
    path('ticket', views.CreateTicketView.as_view(), name='ticket_creation'),
    path('', views.HomesIndexView.as_view(), name='index'),
]
