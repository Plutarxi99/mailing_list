from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'avatar', 'is_active', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Чтобы скрыть пароль в профиле
        self.fields['password'].widget = forms.HiddenInput()