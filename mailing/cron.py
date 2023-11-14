import calendar

from django.utils.timezone import now
from mailing.services.cron import get_tuple_client, change_status_mailing, create_default_log, \
    send_mail_condition_and_log_days
from mailing.models import MailingSetting


def my_scheduled_job():
    m_set = MailingSetting.objects.all()
    for sail in m_set:

        # получение идентификатора для получения кортежа клиентов
        mailing_pk = sail.pk

        # Обновляем статус рассылки, зависит от настоящего времени
        change_status_mailing(sail.pk)

        # Если флаг ссылки запущен, то запускается ссылка
        if sail.is_status == 'run':

            # создание дефолтных логов, для заполнения нулевого лога
            create_default_log(mailing_pk)
            #  получение кортежа клиента
            email_list_client = get_tuple_client(mailing_pk)
            # Получение темы и тело сообщения
            topic = sail.mailing_message_name.topic
            body = sail.mailing_message_name.body


            # Если флаг установлен на каждый день и время рассылки больше времени, чем сейчас
            if sail.frequency == 'day':
                send_mail_condition_and_log_days(mailing_pk, 1, topic, body, email_list_client)
            elif sail.frequency == 'week':
                send_mail_condition_and_log_days(mailing_pk, 7, topic, body, email_list_client)
            elif sail.frequency == 'month':
                # Получение дней в месяце
                days_in_month = calendar.monthrange(year=now().year, month=now().month)[1]
                send_mail_condition_and_log_days(mailing_pk, days_in_month, topic, body, email_list_client)

        elif sail.is_status == 'create':
            print('Рассылка создана')
            pass
        else:
            print('Рассылка закончилась')
            pass
