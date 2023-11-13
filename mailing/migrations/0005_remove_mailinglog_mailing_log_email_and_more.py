# Generated by Django 4.2.7 on 2023-11-08 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_client_mailing_set_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglog',
            name='mailing_log_email',
        ),
        migrations.AddField(
            model_name='client',
            name='mailing_log_last_try',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.mailinglog', verbose_name='последняя попытка'),
        ),
    ]
