import calendar

import datetime

from django.utils.timezone import now
from mailing.services.cron import get_tuple_client, change_status_mailing, create_default_log, \
    send_mail_condition_and_log_days
from mailing.models import MailingSetting


def my_scheduled_job():
    m_set = MailingSetting.objects.all()
    for sail in m_set:
        # получение идентификатора для получения списка клиентов и получение списка клиента
        mailing_pk = sail.pk
        email_list_client = get_tuple_client(mailing_pk)
        # Получение темы и тело сообщения
        topic = sail.mailing_message_name.topic
        body = sail.mailing_message_name.body

        # Обновляем статус рассылки, зависит от настоящего времени
        change_status_mailing(sail.pk)

        # Если флаг ссылки запущен, то запускается ссылка
        if sail.is_status == 'run':

            create_default_log(mailing_pk)
            mail_time = sail.date_mailing

            # Если флаг установлен на каждый день и время рассылки больше времени, чем сейчас
            if sail.frequency == 'day':
                print('day')
                send_mail_condition_and_log_days(mailing_pk, 1, topic, body, email_list_client)
            elif sail.frequency == 'week':
                print('week')
                send_mail_condition_and_log_days(mailing_pk, 7, topic, body, email_list_client)
            elif sail.frequency == 'month':
                print('month')
                # Получение дней в месяце
                days_in_month = calendar.monthrange(year=now().year, month=now().month)[1]
                send_mail_condition_and_log_days(mailing_pk, days_in_month, topic, body, email_list_client)

        elif sail.is_status == 'create':
            print('Рассылка создана')
            pass
        else:
            print('Рассылка закончилась')
            pass

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
    # def send_mail_condition_and_log(pk: int, days: int, topic: str, body: str, email_list_client: list) -> None:
    #     """
    #     Проверка условий и запись логов
    #     @param pk(int): идентификатор распродажи
    #     @param days: разница в днях между последней попыткой и сегодняшней датой
    #     @param topic: тема сообщения
    #     @param body: тело сообщения
    #     @param email_list_client: список получателей
    #     """
    #     # mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    #     # last_try = mailingsetting_item.mailing_log.mailing_log_last_try
    #     # delta = now() - last_try
    #     # print(delta.days)
    #     # if delta.days >= days:
    #     #     print('отправка сообщений')
    #     # Отправка рассылки
    #     # mailing_send_mail(
    #     #     mailing_message_topic=topic,
    #     #     mailing_message_body=body,
    #     #     list_client=email_list_client
    #     # )
    #     # create_log(pk=pk, mailing_log_last_try=now(), mailing_log_is_status_try=True, mailing_log_response_server='200')
    #     mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    #     timedate_mailing = mailingsetting_item.mailing_set_date
    #     timedate_now = now()
    #     print(mailingsetting_item.mailing_set_name)
    #     print(timedate_mailing, 'дата рассылки')
    #     print(timedate_now, 'дата на данный момент')
    #     # time.struct_time(tm_year=2023, tm_mon=11, tm_mday=9, tm_hour=18, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=313, tm_isdst=-1) время рассылки получение значений
    #     timedate_mailing_tuple_isocalendar = datetime.datetime.timetuple(timedate_mailing)
    #     timedate_now_tuple = timedate_now.timetuple()
    #     print(timedate_mailing_tuple_isocalendar, 'время рассылки получение значений')
    #     print(timedate_now_tuple, 'время сейчас получение значений')
    #     print(timedate_mailing, 'секунды время рассылки')
    #
    #     delta_datetime_mail = timedate_mailing - timedate_now
    #     print(delta_datetime_mail, 'разница дат время сейчас и время рассылки')
    #
    #     delta_datetime_second_mail = delta_datetime_mail.seconds
    #     print(delta_datetime_second_mail, 'разница в секундах до рассылки')
    #     current_time = datetime.timedelta(00, 120, 00).seconds
    #
    #     if timedate_mailing_tuple_isocalendar.tm_yday == timedate_now_tuple.tm_yday and delta_datetime_second_mail <= current_time:
    #         print('первое условие выполнения, что день и месяц совпадают')

    # current_time = datetime.timedelta(00, 120, 00).seconds
    # print(current_time, 'установка времени')
    # if delta_datetime_second_mail <= current_time:
    #     print('Рассылка началась')
    #     time.sleep(delta_datetime_second_mail)
    #     print(now())
    #     delta_second_sleep = timedate_now - timedate_mailing
    #     print(delta_second_sleep, 'разница в дате')
    #     print(delta_second_sleep.seconds, 'разница в секундах')
    # else:
    #     print('Время ещё не наступило для рассылки')

    # time.sleep(second_sleep)
    # datatime_send_mail = time_mail + now().date()
    # delta = now() - time_mail
    # print(datatime_send_mail.days)
    # if delta.days >= days:
    #     print('отправка сообщений')
    # Отправка рассылки
    # mailing_send_mail(
    #     mailing_message_topic=topic,
    #     mailing_message_body=body,
    #     list_client=email_list_client
    # )
    # create_log(pk=pk, mailing_log_last_try=now(), mailing_log_is_status_try=True, mailing_log_response_server='200')
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
