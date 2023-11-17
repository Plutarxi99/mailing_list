import uuid
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('mailing:mailing_list')


class LogoutView(BaseLogoutView):
    pass


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    # Избавиться от входящего pk. Редактировать текущего пользователя
    def get_object(self, queryset=None):
        return self.request.user

    # def form_valid(self, form):
    # self.object = form.save()
    # print(self.object)
    # self.object.user_permissions.set([34]) # "mailing.change_mailingsetting"
    # self.object.user_permissions.set([30]) # "mailing.change_mailingmessage"
    # self.object.user_permissions.set([38]) # "mailing.change_client"
    # self.object.save()
    # return super().form_valid(form)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        # self.object = form.save()
        # self.object.user_permissions.set([34]) # "mailing.change_mailingsetting"
        # self.object.user_permissions.set([30]) # "mailing.change_mailingmessage"
        # self.object.user_permissions.set([38]) # "mailing.change_client""
        # self.object.save()
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = reverse_lazy("users:confirm_email", kwargs={"uidb64": uid, "token": token})

        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://127.0.0.1:8000{activation_url}',
            settings.SERVER_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class UserActiveTemplateView(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'users/user_active.html'
    permission_required = 'users.change_user'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['object_list'] = User.objects.all()
        return self.render_to_response(context)


def is_active_user(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True
    user_item.save()

    return redirect(reverse('users:user_active'))
