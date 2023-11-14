import random
from random import randint

from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from journal.models import Journal
from mailing.forms import MailingSettingForm, ClientFormMailingMailingMessage, ClientForm, MailingMessageForm
from mailing.models import Client, MailingSetting, MailingMessage, MailingLog


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser: # self.request.user.groups.filter(name='Manager').exists() or
            return queryset
        else:
            return queryset.filter(client_owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        """
        Сохранения владельца рассылки и его прикрепление к рассылке
        @param form:
        @return:
        """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')
    form_class = ClientForm


class MailingSettingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):
        """
        Сохранения владельца рассылки и его прикрепление к рассылке
        @param form:
        @return:
        """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingListView(LoginRequiredMixin, ListView):
    model = MailingSetting

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(mailing_set_owner=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingSettingUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailingsetting'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     # print(self.object)
    #     return self.object

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        elif self.object.owner != self.request.user:
            raise Http404
        else:
            return self.object

    # def has_permission(self):
    #     """
    #     Если у пользователя нет прав на редактирование выдаёт ошибку 403
    #     """
    #     perms = self.get_permission_required()
    #     product: Product = self.get_object()
    #     return self.request.user == product.product_creator
    # def get_form(self, **kwargs):
    #     """
    #     Метод для скрытия полей редактирования продукта в edit, если пользователь не его создатель
    #     @param **kwargs:
    #     """
    # form = super().get_form()
    # if self.request.user != form.instance.product_creator:
    # сравниваем авторизированного пользователя с создателем продукта
    # enabled_fields = set()  # метод для добавления полей для чего ???
    # # if self.request.user.has_perm(
    # #         'catalog.change_name'):  # если у пользователя есть права на редактирования то разрешаем редактирование этого пользователя
    # #     enabled_fields.add('name')  # добавляем поле для редактирования
    # if self.request.user.has_perm('catalog.change_description'):
    #     enabled_fields.add('description')
    # # if self.request.user.groups.filter(name='Manager').exists(): # Если пользователь принадлежит к группе "Manager", то ему можно изменять поля
    # #     enabled_fields.add('is_published')  # добавляем поле для редактирования
    #
    # if self.request.user.is_superuser:
    #     enabled_fields.add('price')  # добавляем поле для редактирования
    #     enabled_fields.add('category')  # добавляем поле для редактирования
    #     enabled_fields.add('is_published')  # добавляем поле для редактирования
    #
    # for field_name in enabled_fields.symmetric_difference(form.fields):
    #     form.fields[field_name].disabled = True
    #     form.errors.pop(field_name, None)

    # return form


class MailingSettingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSetting
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = MailingSetting
    permission_required = 'mailing.view_mailingsetting'


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_message_list')


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_message_list')


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:mailing_message_list')




class HomeTemplateView(TemplateView):
    template_name = 'mailing/home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['mailing_setting_run'] = MailingSetting.objects.filter(mailing_set_is_status='run')
        context['client'] = Client.objects.all()
        context['journal'] = Journal.objects.order_by('?')[:3]
        return self.render_to_response(context)
