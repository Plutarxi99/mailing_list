import datetime
from django.conf import settings
from django.utils import timezone

from config.settings import NULLABLE
from django.db import models


class MailingMessage(models.Model):
    topic = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.topic}'

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылки'


class MailingLog(models.Model):
    name = models.CharField(max_length=300, verbose_name='названия рассылки лога', **NULLABLE)
    last_try = models.DateTimeField(default=0, verbose_name='последняя попытка', **NULLABLE)
    is_status_try = models.BooleanField(verbose_name='статус попытки', **NULLABLE)
    response_server = models.TextField(verbose_name='ответ сервера', **NULLABLE)
    count_send_mail = models.IntegerField(default=0, verbose_name="количество отправленных рассылок")

    def __str__(self):
        return f' {self.last_try} {self.response_server}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'


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

    name = models.CharField(max_length=200, verbose_name='Названия рассылки')
    date_mailing = models.DateTimeField(default=timezone.now, verbose_name='дата рассылки')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='начало рассылки')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='конец рассылки')
    frequency = models.CharField(choices=FREQUENCY, verbose_name='периодичность', **NULLABLE)
    is_status = models.CharField(choices=STATUS, verbose_name='статус рассылки', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='создатель рассылки')

    mailing_message_name = models.ForeignKey(MailingMessage, on_delete=models.CASCADE,
                                             verbose_name='название рассылки сообщения')

    mailing_log = models.ForeignKey(MailingLog, on_delete=models.CASCADE, verbose_name='mailing_log')

    def __init__(self, *args, **kwargs):
        super(MailingSetting, self).__init__(*args, **kwargs)
        self._is_status = self.is_status
        self._start_time = self.start_time
        self._end_time = self.end_time

    def save(self, *args, **kwargs):
        """
        Для установки автоматического статуса рассылки
        @param args:
        @param kwargs:
        @return:
        """
        time_now = datetime.datetime.now().timestamp()
        if time_now < self.start_time.timestamp():
            self.is_status = 'create'
        elif self.start_time.timestamp() < time_now < self.end_time.timestamp():
            self.is_status = 'run'
        else:
            self.is_status = 'finish'
        super(MailingSetting, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.start_time} - {self.end_time})'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'


class Client(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    owner = models.ManyToManyField(MailingSetting, verbose_name='относится к рассылке')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'