from django.db import models
from django.template.defaultfilters import slugify

from config.settings import NULLABLE


class Journal(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    picture = models.ImageField(upload_to='pictures_journal/', verbose_name='Изображение(превью)', **NULLABLE)
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    published_is = models.BooleanField(default=False, verbose_name='признак публикации')
    count_view = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} ({self.data_create} {self.count_view})'

    class Meta:
        verbose_name = 'журнал'
        verbose_name_plural = 'журналы'
