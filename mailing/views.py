from urllib.parse import urlparse

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import resolve_url
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from journal.models import Journal
from mailing.forms import MailingSettingForm, ClientForm, MailingMessageForm
from mailing.models import Client, MailingSetting, MailingMessage


class MailingSettingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')

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
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class MailingSettingUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailingsetting'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Manager').exists():
            return self.object
        elif self.object.owner != self.request.user:
            raise Http404
        else:
            return self.object

    def get_form(self, **kwargs):
        form = super().get_form()
        if not form.instance.owner == self.request.user or self.request.user.is_superuser:
            if self.request.user.groups.filter(name='Manager').exists():
                enabled_fields = set()
                enabled_fields.add('is_active_mailing')
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form


class MailingSettingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSetting
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSetting


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(created_client=self.request.user)


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
        self.object.created_client = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class ClientUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')
    form_class = ClientForm
    permission_required = 'mailing.change_client'

    def get_form(self, **kwargs):
        form = super().get_form()
        if not form.instance.created_client == self.request.user or self.request.user.is_superuser:
            if self.request.user.groups.filter(name='Manager').exists():
                enabled_fields = set()
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form


class MailingMessageListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = MailingMessage
    permission_required = 'mailing.view_mailingmessage'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.groups.filter(name='Manager').exists() or self.request.user.is_superuser:
            return queryset
        else:
            pk_email = self.request.user
            pk_mailing = MailingSetting.objects.get(owner=pk_email).mailing_message_name.pk
            return queryset.filter(pk=pk_mailing)


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_message_list')

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


class MailingMessageUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_message_list')
    permission_required = 'mailing.change_mailingmessage'

    def get_form(self, **kwargs):
        form = super().get_form()
        if not form.instance.owner == self.request.user or self.request.user.is_superuser:
            if self.request.user.groups.filter(name='Manager').exists():
                enabled_fields = set()
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:mailing_message_list')


class HomeTemplateView(TemplateView):
    template_name = 'mailing/home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['mailing_setting_run'] = MailingSetting.objects.filter(is_status='run')
        context['client'] = Client.objects.all()
        context['journal'] = Journal.objects.filter(published_is=False).order_by('?')[:3]
        return self.render_to_response(context)
