from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from journal.models import Journal
from mailing.forms import MailingSettingForm, ClientForm, MailingMessageForm
from mailing.models import Client, MailingSetting, MailingMessage


class MailingSettingCreateView(LoginRequiredMixin, CreateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        """
        Переопредяем метод для получения почты владельца ,то есть того кто авторизован
        и сохраняем в переменную для получения в forms.py queryset, которые фильтруются по владельцу
        @return: kwargs
        """
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def form_valid(self, form):
        """
        Сохранения владельца рассылки и его прикрепление к рассылке
        @param form:
        @return:
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingSettingListView(LoginRequiredMixin, ListView):
    model = MailingSetting

    def get_queryset(self, *args, **kwargs):
        """
        Получение данных по владельцу или получение всех рассыылок, если ты Manager или superuser
        @param args:
        @param kwargs:
        @return:queryset
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.has_one_of_groups('Manager') or user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class MailingSettingUpdateView(UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = MailingSetting
    form_class = MailingSettingForm
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailingsetting'

    def get_form_kwargs(self):
        """
        Переопредяем метод для получения почты владельца ,то есть того кто авторизован
        и сохраняем в переменную для получения в forms.py queryset, которые фильтруются по владельцу
        @return: kwargs
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        """
        Получение данных по владельцу или получение всех рассыылок, если ты Manager или superuser
        @param args:
        @param kwargs:
        @return:queryset
        """
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.has_one_of_groups('Manager') or user.is_superuser:
            return self.object
        elif self.object.owner != user:
            raise Http404
        else:
            return self.object

    def get_form(self, **kwargs):
        """
        Получение формы без ограничений, если ты владалец данных, иначе
        ты получаешь форму с невозмодностью редактировать поля
        @param kwargs:
        @return:
        """
        form = super().get_form()
        user = self.request.user
        if not form.instance.owner == user or self.request.user.is_superuser:
            if user.has_one_of_groups('Manager') or user.is_superuser:
                enabled_fields = set()
                enabled_fields.add('is_active_mailing')
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form

    def test_func(self):
        """
        Проверка если пользваотель владелец, суперпользователь или Manager
        пропускает к редактированию
        @return:
        """
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.owner or user.has_one_of_groups('Manager') or user.is_superuser:
            return True
        return False


class MailingSettingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSetting
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingDetailView(LoginRequiredMixin, DetailView):
    model = MailingSetting


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self, *args, **kwargs):
        """
        Получение данных по владельцу или получение всех рассыылок, если ты Manager или superuser
        @param args:
        @param kwargs:
        @return:queryset
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.has_one_of_groups('Manager') or user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


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
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class ClientUpdateView(UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')
    form_class = ClientForm
    permission_required = 'mailing.change_client'

    def get_form(self, **kwargs):
        """
        Получение формы без ограничений, если ты владалец данных, иначе
        ты получаешь форму с невозмодностью редактировать поля
        @param kwargs:
        @return:
        """
        form = super().get_form()
        user = self.request.user
        if not form.instance.owner == user or user.is_superuser:
            if user.has_one_of_groups('Manager'):
                enabled_fields = set()
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form

    def test_func(self):
        """
        Проверка если пользваотель владелец, суперпользователь или Manager
        пропускает к редактированию
        @return:
        """
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.owner or user.has_one_of_groups('Manager') or user.is_superuser:
            return True
        return False


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage

    def get_queryset(self, *args, **kwargs):
        """
        Получение данных по владельцу или получение всех рассыылок, если ты Manager или superuser
        @param args:
        @param kwargs:
        @return:queryset
        """
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.has_one_of_groups('Manager') or user.is_superuser:
            return queryset
        else:
            return queryset.filter(owner=user)


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
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingMessageUpdateView(UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:mailing_message_list')
    permission_required = 'mailing.change_mailingmessage'

    def get_form(self, **kwargs):
        """
        Получение формы без ограничений, если ты владалец данных, иначе
        ты получаешь форму с невозмодностью редактировать поля
        @param kwargs:
        @return:
        """
        form = super().get_form()
        user = self.request.user
        if not form.instance.owner == user or user.is_superuser:
            if user.has_one_of_groups('Manager'):
                enabled_fields = set()
                for field_name in enabled_fields.symmetric_difference(form.fields):
                    form.fields[field_name].disabled = True
                    form.errors.pop(field_name, None)
        return form

    def test_func(self):
        """
        Проверка если пользваотель владелец, суперпользователь или Manager
        пропускает к редактированию
        @return:
        """
        self.object = self.get_object()
        user = self.request.user
        if user == self.object.owner or user.has_one_of_groups('Manager') or user.is_superuser:
            return True
        return False


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:mailing_message_list')


class HomeTemplateView(TemplateView):
    template_name = 'mailing/home.html'

    def get(self, request, *args, **kwargs):
        """
        Отдача данных из базы данных для отображения на главной страницы
        @param request:
        @param args:
        @param kwargs:
        @return:
        """
        context = self.get_context_data(**kwargs)
        context['mailing_setting_run'] = MailingSetting.objects.filter(is_status='run')
        context['client'] = Client.objects.all()
        context['journal'] = Journal.objects.filter(published_is=False).order_by('?')[:3]
        return self.render_to_response(context)
