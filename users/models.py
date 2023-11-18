from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from config.settings import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    avatar = models.ImageField(upload_to='users_avatar/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='номер телефона', **NULLABLE)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'