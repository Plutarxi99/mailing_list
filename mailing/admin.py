from django.contrib import admin

from mailing.models import Client, MailingSetting, MailingMessage, MailingLog


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'is_status_try', 'response_server', 'count_send_mail', 'name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment',)


@admin.register(MailingSetting)
class MailingSettingAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_mailing', 'next_time_run', 'start_time', 'end_time', 'frequency', 'is_status',
        'mailing_message_name',
        'mailing_log',)

    def get_readonly_fields(self, request, obj=None):
        print(request.user.groups.filter(name='Manager').exists())
        if request.user.groups.filter(name='Manager').exists():
            return ['name', 'date_mailing', 'next_time_run', 'start_time', 'end_time', 'frequency', 'is_status', 'owner', 'mailing_message_name', 'mailing_log', 'client', ]
        return self.readonly_fields
