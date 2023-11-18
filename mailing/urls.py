from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, \
    MailingSettingCreateView, MailingSettingListView, MailingSettingUpdateView, MailingSettingDeleteView, \
    ClientCreateView, ClientDeleteView, ClientUpdateView, MailingMessageListView, MailingMessageCreateView, \
    MailingMessageDeleteView, MailingMessageUpdateView, MailingSettingDetailView, HomeTemplateView

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(60)(MailingSettingListView.as_view()), name='mailing_list'),
    path('mailing/<int:pk>/update/', MailingSettingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', MailingSettingDeleteView.as_view(), name='mailing_delete'),
    path('mailing/create/', MailingSettingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/detail/', MailingSettingDetailView.as_view(), name='mailing_detail'),

    path('client/list/', cache_page(60)(ClientListView.as_view()), name='list_client'),
    path('client/<int:pk>/view/', ClientDetailView.as_view(), name='client_view'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),

    path('message/list/', cache_page(60)(MailingMessageListView.as_view()), name='mailing_message_list'),
    path('message/create/', MailingMessageCreateView.as_view(), name='mailing_message_create'),
    path('message/<int:pk>/delete/', MailingMessageDeleteView.as_view(), name='mailing_message_delete'),
    path('message/<int:pk>/update/', MailingMessageUpdateView.as_view(), name='mailing_message_update'),

    path('home/', HomeTemplateView.as_view(), name='home'),
]
