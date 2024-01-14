from django.urls import path

from . import views


urlpatterns = [
    path('homes', views.HomesIndexView.as_view(), name='homes'),
    path('contacts', views.HomesIndexView.as_view(), name='contacts'),
    path('ticket', views.CreateTicketView.as_view(), name='ticket_creation'),
    path('', views.HomesIndexView.as_view(), name='index'),
]
