# Generated by Django 4.2.7 on 2023-11-17 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailingsetting_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingsetting',
            options={'verbose_name': 'Настройка рассылки', 'verbose_name_plural': 'Настройки рассылки'},
        ),
    ]
