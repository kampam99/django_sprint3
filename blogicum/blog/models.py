from django.contrib.auth.models import User
from django.db import models


class IsPublishedAndCreatedAt(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Post(IsPublishedAndCreatedAt):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в '
                   'будущем — можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        verbose_name='Автор публикации',
        to=User,
        on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        verbose_name='Местоположение',
        to='Location',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to='Category',
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Category(IsPublishedAndCreatedAt):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(IsPublishedAndCreatedAt):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name
