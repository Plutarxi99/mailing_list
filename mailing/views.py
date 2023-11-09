import datetime

from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingSettingForm, ClientFormMailingMailingMessage
from mailing.models import Client, MailingSetting, MailingMessage, MailingLog
from config.settings import SERVER_EMAIL


class ClientListView(ListView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        return queryset


class ClientDetailView(DetailView):
    model = Client


class MailingSettingCreateView(CreateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:list_client')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # MailingMessageFormset = inlineformset_factory(MailingSetting, MailingMessage, form=ClientFormMailingMailingMessage, extra=1)
        # obj = self.object
        # if self.request.method == 'POST':
        #     context_data['formset'] = MailingMessageFormset(self.request.POST, instance=obj)
        # else:
        #     context_data['formset'] = MailingMessageFormset(instance=obj)
        return context_data


class MailingSettingListView(ListView):
    model = MailingSetting

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # queryset = queryset.filter(published_is=False)
        # mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
        # time_now = datetime.datetime.now().timestamp()  # получение сегодняшней даты и время
        # time_mailing_start = mailingsetting_item.mailing_set_start_time.timestamp()  # получение времени начало рассылки
        # time_mailing_end = mailingsetting_item.mailing_set_end_time.timestamp()  # получение времени конца рассылки
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingSettingUpdateView(UpdateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')
    
    def get_object(self, queryset=None):
        obj = MailingSetting.objects.get(id=self.kwargs['id'])
        return obj
        # self.object = super().get_object(queryset)
        # print(self.object)
        # return self.object


class MailingSettingDeleteView(DeleteView):
    model = MailingSetting
    success_url = reverse_lazy('mailing:mailing_list')


def is_publish(pk):
    mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    time_now = datetime.datetime.now().timestamp()  # получение сегодняшней даты и время
    time_mailing_start = mailingsetting_item.mailing_set_start_time.timestamp()  # получение времени начало рассылки
    time_mailing_end = mailingsetting_item.mailing_set_end_time.timestamp()  # получение времени конца рассылки

    if time_now < time_mailing_start:
        mailingsetting_item.mailing_set_is_status = 'create'
    elif time_mailing_start < time_now <= time_mailing_end:  # если сегодня входит в промежуток времени рассылок
        mailingsetting_item.mailing_set_is_status = 'run'
    else:
        mailingsetting_item.mailing_set_is_status = 'finish'

    mailingsetting_item.save()
    #
    # return redirect(reverse('mailing:list'))


def mailing_send_mail(
        mailing_message_topic,
        mailing_message_body,
        list_client
):
    send_mail(
        subject=mailing_message_topic,
        message=mailing_message_body,
        from_email=SERVER_EMAIL,
        recipient_list=list_client
    )
