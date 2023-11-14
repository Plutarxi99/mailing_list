import datetime

from django.core.mail import send_mass_mail
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from mailing.models import Client, MailingSetting, MailingLog
from config.settings import SERVER_EMAIL

time_now = datetime.datetime.now()  # получение сегодняшней даты и время


def send_mail_condition_and_log_days(pk: int, days: int, topic: str, body: str, email_tuple_client: list) -> None:
    """
    Проверка условий и запись логов
    @param pk(int): идентификатор распродажи
    @param days: разница в днях между последней попыткой и сегодняшней датой
    @param topic: тема сообщения
    @param body: тело сообщения
    @param email_tuple_client: кортеж получателей
    """
    mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)

    # Получение даты рассылки и даты следующей рассылки
    date_mailing = mailingsetting_item.date_mailing
    next_time_run = mailingsetting_item.next_time_run

    # Если сейчас лежит во временном отрезке между датой рассылки и следующей даты рассылки,
    # то срабатывает скрипт отправки сообщений
    if date_mailing <= now() <= next_time_run:

        # Отправка рассылки
        mail = mailing_send_mail(
            mailing_message_topic=topic,
            mailing_message_body=body,
            list_client=email_tuple_client
        )

        # Если отправка не вызвала ошибок, то дата следующей отправки меняется
        if mail['status']:
            # Установка и сохранения новой даты отправки с учетом периодичности
            new_date_mailing = date_mailing + datetime.timedelta(days=days)
            mailingsetting_item.date_mailing = new_date_mailing
            mailingsetting_item.save()

        count_send_mail = mailingsetting_item.mailing_log.count_send_mail
        count_send_mail += 1
        # Создания логов
        mailing_log_name = mailingsetting_item.name + f' №{count_send_mail}'
        create_log(pk=pk, last_try=now(), is_status_try=mail['status'],
                   response_server=mail["response"],
                   count_send_mail=count_send_mail,
                   name=mailing_log_name)

    else:
        pass


def create_log(pk: int, last_try: str, is_status_try: bool,
               response_server: str, count_send_mail: int,
               name: str) -> None:
    """
    Создания лога к объекту рассылки
    @param pk: идентификатор объекта модели MailingSetting
    @param last_try: последняя попытка отправки
    @param is_status_try: состояние отправки
    @param mresponse_server: ответ сервера
    @return:
    """
    mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    maillog_object = MailingLog(last_try=last_try,
                                is_status_try=is_status_try,
                                response_server=response_server,
                                count_send_mail=count_send_mail,
                                name=name)
    maillog_object.save()
    mail_log_pk = MailingLog.objects.last().pk
    mail_log_obj = MailingLog.objects.get(pk=mail_log_pk)
    mailingsetting_item.mailing_log = mail_log_obj
    mailingsetting_item.save()


def create_default_log(pk: int) -> None:
    """
    Создание дефолтных логов
    @param pk:
    @return:
    """
    mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    mail_log = mailingsetting_item.mailing_log
    if mail_log:
        pass
    else:
        create_log(pk=pk, last_try=now(), is_status_try=False,
                   response_server='404', name='default', count_send_mail=0)


def change_status_mailing(pk: int) -> None:
    """
    Меняет статут рассылки, в зависимости от настоящего времени меняет статус модели MailingSetting
    :param pk(int): идентификатор распродажи
    """
    mailingsetting_item = get_object_or_404(MailingSetting, pk=pk)
    time_mailing_start = mailingsetting_item.start_time  # получение времени начало рассылки
    time_mailing_end = mailingsetting_item.end_time  # получение времени конца рассылки

    if now() < time_mailing_start:
        mailingsetting_item.is_status = 'create'
    elif time_mailing_start < now() <= time_mailing_end:  # если сегодня входит в промежуток времени рассылок
        mailingsetting_item.is_status = 'run'
    else:
        mailingsetting_item.is_status = 'finish'
    mailingsetting_item.save()


def get_tuple_client(list_client_pk: int) -> tuple:
    """
    Получение кортежа клиентов, которые относятся к распродаже
        example:
            ('egor.shievanov@gmail.com', 'test@test.com')
    @param list_client_pk: идентификатор распродажи, полученный из ClientList
    @return: tuple
    """
    list_email_pk = MailingSetting.client.through.objects.values().filter(mailingsetting_id=list_client_pk).values_list(
        'client_id', flat=True)
    email_list_client = Client.objects.filter(id__in=[*list_email_pk]).values_list(
        'email', flat=True)
    emails = tuple(email_list_client)
    return emails


def mailing_send_mail(
        mailing_message_topic: object,
        mailing_message_body: object,
        list_client: object
) -> dict:
    """
    Функция для отправки писем
    @param mailing_message_topic: тема сообщения
    @param mailing_message_body: тело сообщения
    @param list_client: кортеж клиентов, которым отправятся рассылка
    """
    global BaseException
    message = (
        mailing_message_topic,
        mailing_message_body,
        SERVER_EMAIL,
        list_client,
    )
    try:
        send_mass_mail((message,), fail_silently=False)
        return {'status': True, 'response': "Сервер отработал как надо"}
    except BaseException as error:
        return {'status': False, 'response': error}
