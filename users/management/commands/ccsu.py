from django.conf import settings
from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    # Создание суперюзера из-за того, что мы переопределили создание юзера. Мы не можно создать его командой createsuperuser

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email=settings.SUPERUSER_EMAIL,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        if created or not user.check_password(settings.SUPERUSER_PASSWORD):
            user.set_password(settings.SUPERUSER_PASSWORD)
            user.save()