from django.urls import path

from mailing.apps import MailingConfig
from mailing.models import Client
from mailing.views import ClientListView, ClientDetailView, \
    MailingSettingCreateView, MailingSettingListView, MailingSettingUpdateView, MailingSettingDeleteView, \
    ClientCreateView, ClientDeleteView, ClientUpdateView, MailingMessageListView, MailingMessageCreateView, \
    MailingMessageDeleteView, MailingMessageUpdateView, MailingSettingDetailView, HomeTemplateView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='list_client'),
    path('mailing_list/', MailingSettingListView.as_view(), name='mailing_list'),
    path('mailing_update/<int:pk>', MailingSettingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingSettingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_create/', MailingSettingCreateView.as_view(), name='mailing_create'),
    path('mailing_detail/<int:pk>/', MailingSettingDetailView.as_view(), name='mailing_detail'),

    path('client_view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),

    path('mailing_message_list/', MailingMessageListView.as_view(), name='mailing_message_list'),
    path('mailing_message_create/', MailingMessageCreateView.as_view(), name='mailing_message_create'),
    path('mailing_message_delete/<int:pk>', MailingMessageDeleteView.as_view(), name='mailing_message_delete'),
    path('mailing_message_update/<int:pk>', MailingMessageUpdateView.as_view(), name='mailing_message_update'),

    path('mailing/', HomeTemplateView.as_view(), name='home'),
]
