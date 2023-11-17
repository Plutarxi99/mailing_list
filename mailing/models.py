import calendar
import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now

from config.settings import NULLABLE
from django.db import models


class MailingMessage(models.Model):
    topic = models.CharField(max_length=100, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='создатель рассылки', **NULLABLE)

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


class Client(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    created_client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='создатель клиента', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


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
    next_time_run = models.DateTimeField(default=timezone.now, verbose_name='дата следующей рассылки')
    start_time = models.DateTimeField(default=timezone.now, verbose_name='начало рассылки')
    end_time = models.DateTimeField(default=timezone.now, verbose_name='конец рассылки')
    frequency = models.CharField(choices=FREQUENCY, verbose_name='периодичность', **NULLABLE)
    is_status = models.CharField(choices=STATUS, verbose_name='статус рассылки', **NULLABLE)
    is_active_mailing = models.BooleanField(default=True, verbose_name='активность рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='создатель рассылки', **NULLABLE)

    mailing_message_name = models.ForeignKey(MailingMessage, on_delete=models.CASCADE,
                                             verbose_name='название рассылки сообщения')

    mailing_log = models.ForeignKey(MailingLog, on_delete=models.SET_NULL, verbose_name='mailing_log', **NULLABLE)

    client = models.ManyToManyField(Client, verbose_name='относится к рассылке')


    def __init__(self, *args, **kwargs):
        super(MailingSetting, self).__init__(*args, **kwargs)
        self._is_status = self.is_status
        self._start_time = self.start_time
        self._end_time = self.end_time
        self._next_time_run = self.next_time_run
        self._date_mailing = self.date_mailing
        self._frequency = self.frequency

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
            if self.frequency == 'day':
                self.next_time_run = self.date_mailing + datetime.timedelta(days=1)
            elif self.frequency == 'week':
                self.next_time_run = self.date_mailing + datetime.timedelta(days=7)
            elif self.frequency == 'month':
                # Получение дней в месяце
                days_in_month = calendar.monthrange(year=now().year, month=now().month)[1]
                self.next_time_run = self.date_mailing + datetime.timedelta(days=days_in_month)
        else:
            self.is_status = 'finish'
        super(MailingSetting, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.start_time} - {self.end_time})'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'
