from django.contrib import admin

from mailing.models import Client, MailingSetting, MailingMessage, MailingLog, ClientList


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('mailing_message_name', 'mailing_message_topic', 'mailing_message_body',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = (
        'mailing_log_last_try', 'mailing_log_is_status_try', 'mailing_log_response_server', 'mailing_log_count_send_mail', 'mailing_log_name')


# @admin.register(MailingLogTest)
# class MailingLogTestAdmin(admin.ModelAdmin):
#     list_display = (
#         'mailing_log_last_try', 'mailing_log_is_status_try', 'mailing_log_response_server',)


@admin.register(ClientList)
class ClientListAdmin(admin.ModelAdmin):
    list_display = ('client_list_name',)


@admin.register(MailingSetting)
class MailingSettingAdmin(admin.ModelAdmin):
    list_display = ('mailing_set_name', 'mailing_set_start_time', 'mailing_set_end_time', 'mailing_set_frequency',
                    'mailing_set_is_status', 'mailing_message_name', 'client_list', 'mailing_log',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'comment',)
