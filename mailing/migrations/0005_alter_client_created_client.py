# Generated by Django 4.2.7 on 2023-11-17 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0004_mailingsetting_is_active_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='создатель клиента'),
        ),
    ]