import datetime
from django.conf import settings
from config.settings import NULLABLE
from django.db import models


class MailingMessage(models.Model):
    mailing_message_name = models.CharField(max_length=200, verbose_name='название рассылки сообщения', unique=True)
    mailing_message_topic = models.CharField(max_length=100, verbose_name='тема письма', **NULLABLE)
    mailing_message_body = models.TextField(verbose_name='тело письма', **NULLABLE)

    def __str__(self):
        return f'{self.mailing_message_name}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class MailingLog(models.Model):
    mailing_log_name = models.CharField(max_length=300, verbose_name='названия рассылки лога', **NULLABLE)
    mailing_log_last_try = models.DateTimeField(default=0, verbose_name='последняя попытка', **NULLABLE)
    mailing_log_is_status_try = models.BooleanField(verbose_name='статус попытки', **NULLABLE)
    mailing_log_response_server = models.TextField(verbose_name='ответ сервера', **NULLABLE)
    mailing_log_count_send_mail = models.IntegerField(default=0, verbose_name="количество отправленных рассылок",
                                                      **NULLABLE)

    def __str__(self):
        return f' {self.mailing_log_last_try} {self.mailing_log_response_server}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'


class ClientList(models.Model):
    client_list_name = models.CharField(max_length=150, verbose_name='название списка клиентов', unique=True)

    def __str__(self):
        return f'{self.client_list_name}'

    class Meta:
        verbose_name = 'Список клиентов'
        verbose_name_plural = 'Списки клиентов'


class MailingSetting(models.Model):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    FREQUENCY = [
        (DAY, 'one_to_day'),
        (WEEK, 'one_to_week'),
        (MONTH, 'one_to_month'),
    ]

    STATUS = [
        ('create', 'mailing_create'),
        ('run', 'mailing_run'),
        ('finish', 'mailing_finish'),
    ]

    mailing_set_name = models.CharField(max_length=200, verbose_name='Названия рассылки', unique=True)
    mailing_set_date = models.DateTimeField(verbose_name='дата рассылки', **NULLABLE)
    mailing_set_start_time = models.DateTimeField(verbose_name='начало рассылки', **NULLABLE)
    mailing_set_end_time = models.DateTimeField(verbose_name='конец рассылки', **NULLABLE)
    mailing_set_frequency = models.CharField(max_length=15, choices=FREQUENCY, verbose_name='периодичность', **NULLABLE)
    mailing_set_is_status = models.CharField(max_length=15, choices=STATUS, verbose_name='статус рассылки', **NULLABLE)
    mailing_set_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                          verbose_name='создатель рассылки')

    mailing_message_name = models.ForeignKey(MailingMessage, on_delete=models.SET_NULL,
                                             verbose_name='название рассылки сообщения', **NULLABLE)

    client_list = models.ForeignKey(ClientList, on_delete=models.SET_NULL, verbose_name='список клиентов', **NULLABLE)

    mailing_log = models.ForeignKey(MailingLog, on_delete=models.SET_NULL, verbose_name='mailing_log', **NULLABLE)

    def __init__(self, *args, **kwargs):
        super(MailingSetting, self).__init__(*args, **kwargs)
        self._mailing_set_is_status = self.mailing_set_is_status
        self._mailing_set_start_time = self.mailing_set_start_time
        self._mailing_set_end_time = self.mailing_set_end_time

    def save(self, *args, **kwargs):
        """
        Для установки автоматического статуса рассылки
        @param args:
        @param kwargs:
        @return:
        """
        time_now = datetime.datetime.now().timestamp()
        if time_now < self.mailing_set_start_time.timestamp():
            self.mailing_set_is_status = 'create'
        elif self.mailing_set_start_time.timestamp() < time_now < self.mailing_set_end_time.timestamp():
            self.mailing_set_is_status = 'run'
        else:
            self.mailing_set_is_status = 'finish'
        super(MailingSetting, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.mailing_set_name} ({self.mailing_set_start_time} - {self.mailing_set_end_time})'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


class Client(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    client_list = models.ForeignKey(ClientList, on_delete=models.SET_NULL, verbose_name='список клиентов', **NULLABLE)

    client_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                     verbose_name='создатель клиента')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
