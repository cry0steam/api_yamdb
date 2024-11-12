from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from .constants import CHAR_FIELD_LIMIT, SLUG_FIELD_LIMIT, SYMBOLS_LIMIT


class User(AbstractUser):
    role = models.CharField("роль", max_length=20, blank=True)


class Genre(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LIMIT,
        unique=True, verbose_name='Слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LIMIT,
        unique=True, verbose_name='Слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        through='TitleGenres',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}, {self.year}, {self.description[:SYMBOLS_LIMIT]}'


class TitleGenres(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
