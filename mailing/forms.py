from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.utils.timezone import now

from mailing.models import MailingSetting, MailingMessage, Client


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class MailingSettingForm(forms.ModelForm):
    class Meta:
        model = MailingSetting
        exclude = ('owner', 'mailing_log', 'is_status', 'next_time_run',)

    def __init__(self, *args, **kwargs):
        # для скрытия выбора выпадающего списка при создании рассылки, только тех данных, кому принадлежат эти данные
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Для того, чтобы пользователь вводил корректно данные в базу данных
        self.fields['date_mailing'].widget = DateTimeInput()
        self.fields['date_mailing'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields['start_time'].widget = DateTimeInput()
        self.fields['start_time'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields['end_time'].widget = DateTimeInput()
        self.fields['end_time'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        # для скрытия выбора выпадающего списка при создании рассылки, только тех данных, кому принадлежат эти данные
        self.fields['mailing_message_name'].queryset = self.fields['mailing_message_name'].queryset.filter(
            owner=user)
        self.fields['client'].queryset = self.fields['client'].queryset.filter(
            owner=user)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in settings.RUSSIAN_BAN_WORDS:
            raise forms.ValidationError('Недопустимое слово')
        return cleaned_data

    def clean_date_mailing(self):
        cleaned_data = self.cleaned_data['date_mailing']
        if cleaned_data < now():
            raise forms.ValidationError('Дата рассылки должна быть больше, чем сейчас')
        return cleaned_data

    def clean_start_time(self):
        cleaned_data = self.cleaned_data['start_time']
        if cleaned_data < now():
            raise forms.ValidationError('Дата начало рассылки должна быть больше, чем сейчас')
        return cleaned_data

    def clean_end_time(self):
        cleaned_data = self.cleaned_data['end_time']
        if cleaned_data < now():
            raise forms.ValidationError('Дата конца рассылки должна быть больше, чем сейчас')
        return cleaned_data


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('created_client',)


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ('owner',)
