from django import forms

from mailing.models import  MailingSetting, MailingMessage


class MailingSettingForm(forms.ModelForm):
    class Meta:
        model = MailingSetting
        fields = '__all__'


class ClientFormMailingMailingMessage(forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'

