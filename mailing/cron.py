import os
import datetime

from config.settings import CRONTIME
from mailing.models import Client, MailingSetting
from mailing.views import mailing_send_mail, ClientListView, MailingSettingUpdateView


def get_list_client(list_client_pk: int) -> list:
    """
    Получение списка клиентов, которые относятся к распродаже
        example:
            ['winter1@test.com', 'winter@test.com']
    @param list_client_pk: идентификатор распродажи, полученный из ClientList
    @return: list
    """
    email_list_client = Client.objects.values_list("email", flat=True).filter(client_list_id=list_client_pk)
    return email_list_client


def my_scheduled_job():
    m_set = MailingSetting.objects.all()
    for sail in m_set:
        list_client_pk = sail.client_list.pk  # получение идентификатора для получения списка клиентов
        email_list_client = get_list_client(list_client_pk)

        # Получение темы и тело сообщения
        # topic = sail.mailing_message_name.mailing_message_topic
        # body = sail.mailing_message_name.mailing_message_body
        mail = MailingSettingUpdateView.get_object(sail)
        print(mail)
        print(sail.mailing_set_is_status)
            # mailing_send_mail(
            #     mailing_message_topic=topic,
            #     mailing_message_body=body,
            #     list_client=email_list_client
            # )






















    # client = Client.objects.filter(client_list_id=1)
    # for cl in client:
    #     print(cl.email)

    # clients = Client.objects.all()
    # for client in clients:  # Запускаем цикл на получение данных
    #     if client.mailing_set_name.mailing_set_is_status == 'run':  # если установлен флаг на рассылки, то запускается цикл на рассылки
    #
    #         time_mailing_start = client.mailing_set_name.mailing_set_start_time.timestamp()  # получение времени начало рассылки
    #         time_mailing_end = client.mailing_set_name.mailing_set_end_time.timestamp()  # получение времени конца рассылки
    #         time_now = datetime.datetime.now().timestamp()  # получение сегодняшней даты и время
    #
    #         if time_now < time_mailing_start:  # сравниваем, что рассылки ещё не началась
    #             print('Рассылка ещё не началась')
    #
    #         elif time_mailing_start < time_now <= time_mailing_end:  # если сегодня входит в промежуток времени рассылок
    #             mailing_set_frequency = client.mailing_set_name.mailing_set_frequency  # получаем период рассылки
    #
    #             if mailing_set_frequency == 'day':  # если рассылка каждый день
    #                 email = client.email  # получаем почту клиента для отправки
    #
    #                 time_send_mail = client.mailing_set_name.mailing_set_time
    #                 # получение время рассылки для отправки сообщения
    #                 time_now_timer = datetime.datetime.now().time()
    #                 # получение времени на данный момент
    #
    #                 time_send_mail_day = datetime.datetime.combine(
    #                     datetime.date.today(), time_send_mail
    #                 )  # получение даты со временем отправки
    #                 time_now_timer_day = datetime.datetime.combine(
    #                     datetime.date.today(), time_now_timer
    #                 )
    #                 # получение даты со временем сейчас
    #
    #                 date_time_difference = time_send_mail_day - time_now_timer_day
    #                 # вычисляем разницу для того, чтобы сравнить время и отправить расссылку
    #
    #                 date_time_difference_in_hours = date_time_difference.total_seconds()
    #                 # получение разницы в секундах
    #
    #                 if abs(int(date_time_difference_in_hours)) < diff_time:
    #                     # если разница меньше установленного промежутка рассылка, то начинается рассылка
    #                     print('Рассылка началась')
    #                     mailing_send_mail(
    #                         mailing_message_topic=client.mailing_set_name.mailing_message_name.mailing_message_topic,
    #                         mailing_message_body=client.mailing_set_name.mailing_message_name.mailing_message_body,
    #                         list_client=[email]
    #                     )
    #                 else:
    #                     print('сегодня рассылка уже отправлена')
    #                     pass
    #
    #                 # client_pk = client.pk
    #                 # print(client.mailinglog_set.all().mailing_log_last_try)
    #
    #
    #             elif mailing_set_frequency == 'week':
    #                 emails = client.email
    #                 print(emails)
    #
    #                 # print(emails)
    #             elif mailing_set_frequency == 'month':
    #                 emails = client.email
    #                 # print(emails)
    #             else:
    #                 pass
    #
    #         elif time_now < time_mailing_end:
    #             print('Расылка закончилась')
    #
    #     elif client.mailing_set_name.mailing_set_is_status == 'create':
    #         print('Успешно создано')
    #
    #     elif client.mailing_set_name.mailing_set_is_status == 'finish':
    #         print('mailing_finish')
    #
    #     else:
    #         print('Error')
    # print('Конец цикла')

    # email = []
    # client = Client.objects.all()
    # for object in client:
    #     email.append(object.email)
    #     mailing_set_status = MailingSetting.mailing_set_is_status
    #     print(mailing_set_status)
    # if mailing_set_status == 'run':
    #     time_mailing_start = MailingSetting.mailing_set_start_time.timestamp()
    #     time_mailing_end = MailingSetting.mailing_set_end_time.timestamp()
    #     time_now = datetime.now().timestamp()
    #     print(time_mailing_start)
    #     print(time_mailing_end)
    #     print(time_now)
    #     if time_now < time_mailing_start:
    #             print('Рассылка ещё не началась')
    #
    #     elif time_mailing_start < time_now <= time_mailing_end:
    #         mailing_set_frequency = MailingSetting.mailing_set_frequency
    #         if mailing_set_frequency == 'day':
    #             email = client.email
    #             time_send_mail = MailingSetting.mailing_set_time
    #             time_now_timer = datetime.now().time()
    #             time_diff = time_send_mail - time_now_timer
    # a = divmod(time_diff.days * 3600 + time_diff.seconds, 60)
    # print(time_send_mail)

    # mailing_send_mail(
    #     mailing_message_topic=client.mailing_set_name.mailing_message_name.mailing_message_topic,
    #     mailing_message_body=client.mailing_set_name.mailing_message_name.mailing_message_body,
    #     list_client=email
    # )
    # elif mailing_set_status == 'create':
    #     print('Успешно создано')
    #
    #
    # elif mailing_set_status == 'finish':
    #     print('mailing_finish')

    # clients = Client.objects.all()
    # for client in clients:
    #
    #     if client.mailing_set_name.mailing_set_is_status == 'run':
    #         time_mailing_start = client.mailing_set_name.mailing_set_start_time.timestamp()
    #         time_mailing_end = client.mailing_set_name.mailing_set_end_time.timestamp()
    #         time_now = datetime.now().timestamp()
    #
    #         if time_now < time_mailing_start:
    #             print('Рассылка ещё не началась')
    #
    #         elif time_mailing_start < time_now <= time_mailing_end:
    #             mailing_set_frequency = client.mailing_set_name.mailing_set_frequency
    #             if mailing_set_frequency == 'day':
    #                 email = client.email
    #                 time_send_mail = client.mailing_set_name.mailing_set_time
    #                 time_now_timer = datetime.now().time()
    #                 time_diff = time_send_mail - time_now_timer
    #                 print(time_diff)
    #
    #
    #
    #                 # mailing_send_mail(
    #                 #     mailing_message_topic=client.mailing_set_name.mailing_message_name.mailing_message_topic,
    #                 #     mailing_message_body=client.mailing_set_name.mailing_message_name.mailing_message_body,
    #                 #     list_client=email
    #                 # )
    #             elif mailing_set_frequency == 'week':
    #                 emails = client.email
    #                 print(emails)
    #             else:
    #                 pass
    #
    #         elif time_now < time_mailing_end:
    #             print('Расылка закончилась')
    #
    #     elif client.mailing_set_name.mailing_set_is_status == 'create':
    #         print('Успешно создано')
    #
    #     elif client.mailing_set_name.mailing_set_is_status == 'finish':
    #         print('mailing_finish')
    #
    #     else:
    #         print('Error')
    # print('Конец цикла')
