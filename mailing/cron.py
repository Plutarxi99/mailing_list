import calendar

from django.utils.timezone import now
from mailing.services.cron import get_tuple_client, change_status_mailing, create_default_log, \
    send_mail_condition_and_log_days
from mailing.models import MailingSetting


def my_scheduled_job():
    m_set = MailingSetting.objects.all()
    for mailingsetting_item in m_set:
        # получение идентификатора для получения кортежа клиентов
        mailing_pk = mailingsetting_item.pk
        # Обновляем статус рассылки, зависит от настоящего времени
        change_status_mailing(mailingsetting_item.pk)
        mailingsetting_item.refresh_from_db()
        if all((
                mailingsetting_item.is_status == 'run',
                mailingsetting_item.is_active_mailing,
        )):
            create_default_log(mailingsetting_item.pk)
        # Если флаг ссылки запущен, то запускается ссылка
        if mailingsetting_item.is_status == 'run' and mailingsetting_item.is_active_mailing:
            #  получение кортежа клиента
            email_list_client = get_tuple_client(mailing_pk)
            # Получение темы и тело сообщения
            topic = mailingsetting_item.mailing_message_name.topic
            body = mailingsetting_item.mailing_message_name.body
            # Если флаг установлен на каждый день и время рассылки больше времени, чем сейчас
            if mailingsetting_item.frequency == 'day':
                send_mail_condition_and_log_days(mailing_pk, 1, topic, body, email_list_client)
            elif mailingsetting_item.frequency == 'week':
                send_mail_condition_and_log_days(mailing_pk, 7, topic, body, email_list_client)
            elif mailingsetting_item.frequency == 'month':
                # Получение дней в месяце
                days_in_month = calendar.monthrange(year=now().year, month=now().month)[1]
                send_mail_condition_and_log_days(mailing_pk, days_in_month, topic, body, email_list_client)
        elif mailingsetting_item.is_status == 'create':
            pass
        else:
            pass
