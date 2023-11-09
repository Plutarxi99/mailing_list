from django.urls import path

from mailing.apps import MailingConfig
from mailing.models import Client
from mailing.views import ClientListView, ClientDetailView, mailing_send_mail, \
    MailingSettingCreateView, MailingSettingListView, MailingSettingUpdateView, MailingSettingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='list_client'),
    path('mailing_list/', MailingSettingListView.as_view(), name='mailing_list'),
    path('mailing_update/<int:pk>', MailingSettingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>', MailingSettingDeleteView.as_view(), name='mailing_delete'),

    path('client_view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client_create/', MailingSettingCreateView.as_view(), name='client_create'),
    path('mailing_send_mail/', mailing_send_mail, name='client_mailing'),
]
