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


class MailingSetting(models.Model):
    FREQUENCY = (
        ('day', 'one_to_day'),
        ('week', 'one_to_week'),
        ('month', 'one_to_month'),
    )

    STATUS = (
        ('create', 'mailing_create'),
        ('run', 'mailing_run'),
        ('finish', 'mailing_finish'),
    )
    mailing_set_name = models.CharField(max_length=200, verbose_name='названия рассылки настроек', unique=True)
    mailing_set_time = models.TimeField(verbose_name='время рассылки', **NULLABLE)
    mailing_set_start_time = models.DateTimeField(verbose_name='начало рассылки', **NULLABLE)
    mailing_set_end_time = models.DateTimeField(verbose_name='конец рассылки', **NULLABLE)
    mailing_set_frequency = models.CharField(max_length=15, choices=FREQUENCY, verbose_name='периодичность', **NULLABLE)
    mailing_set_is_status = models.CharField(max_length=15, choices=STATUS, verbose_name='статус рассылки', **NULLABLE)

    mailing_message_name = models.ForeignKey(MailingMessage, on_delete=models.SET_NULL,
                                             verbose_name='название рассылки сообщения', **NULLABLE)

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

    mailing_set_name = models.ForeignKey(MailingSetting, on_delete=models.SET_NULL, verbose_name='названия рассылки',
                                         **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class MailingLog(models.Model):
    mailing_log_last_try = models.DateTimeField(default=0, verbose_name='последняя попытка', **NULLABLE)
    mailing_log_is_status_try = models.BooleanField(verbose_name='статус попытки', **NULLABLE)
    mailing_log_response_server = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    mailing_log_email = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='email')

    def __str__(self):
        return f'{self.mailing_log_email} {self.mailing_log_last_try} {self.mailing_log_response_server}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
