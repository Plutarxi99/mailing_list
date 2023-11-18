from django.contrib import admin

from mailing.models import Client, MailingSetting, MailingMessage, MailingLog


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('topic', 'body',)

    def get_readonly_fields(self, request, obj=None):
        """
        Для скрытия полей редактированиия в админ панели
        @param request:
        @param obj:
        @return:
        """
        if request.user.is_staff:
            return ['owner', 'body', 'topic']
        return self.readonly_fields


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'is_status_try', 'response_server', 'count_send_mail', 'name',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment',)

    def get_readonly_fields(self, request, obj=None):
        """
        Для скрытия полей редактированиия в админ панели
        @param request:
        @param obj:
        @return:
        """
        if request.user.is_staff:
            return ['created_client', 'comment', 'last_name', 'first_name', 'email']
        return self.readonly_fields


@admin.register(MailingSetting)
class MailingSettingAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'date_mailing', 'next_time_run', 'start_time', 'end_time', 'frequency', 'is_status',
        'mailing_message_name',
        'mailing_log',)

    def get_readonly_fields(self, request, obj=None):
        """
        Для скрытия полей редактированиия в админ панели
        @param request:
        @param obj:
        @return:
        """
        if request.user.is_staff:
            return ['name', 'date_mailing', 'next_time_run', 'start_time', 'end_time', 'frequency', 'is_status',
                    'owner', 'mailing_message_name', 'mailing_log', 'client', ]
        return self.readonly_fields
