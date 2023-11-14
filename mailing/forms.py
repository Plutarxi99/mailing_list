from django import forms
from django.contrib.admin import widgets

from mailing.models import MailingSetting, MailingMessage, Client


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class MailingSettingForm(forms.ModelForm):
    class Meta:
        model = MailingSetting
        # fields = '__all__'
        exclude = ('mailing_set_owner', 'mailing_log', 'mailing_set_is_status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mailing_set_date'].widget = DateTimeInput()
        self.fields['mailing_set_date'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields['mailing_set_start_time'].widget = DateTimeInput()
        self.fields['mailing_set_start_time'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]
        self.fields['mailing_set_end_time'].widget = DateTimeInput()
        self.fields['mailing_set_end_time'].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MailingMessageForm(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'


class ClientFormMailingMailingMessage(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'

