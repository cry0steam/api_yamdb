from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .constants import CHAR_FIELD_LIMIT, SLUG_FIELD_LIMIT, SYMBOLS_LIMIT

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    role = models.CharField(
        'роль', choices=ROLE_CHOICES, default=USER, max_length=20, blank=True
    )
    confirmation_code = models.CharField(
        'код подтверждения', max_length=255, blank=False, default='012345'
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимый символ',
            )
        ],
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(instance)
        instance.confirmation_code = confirmation_code
        instance.save()


class Genre(models.Model):
    """Модель для имени и описания жанра."""

    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LIMIT, unique=True, verbose_name='Слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для имени и описания категории."""

    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LIMIT, unique=True, verbose_name='Слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель, описывающая произведение."""

    name = models.CharField(
        max_length=CHAR_FIELD_LIMIT, verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания',
        validators=[MaxValueValidator(timezone.now().year)],
    )
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        through='TitleGenres',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
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
        Genre, null=True, blank=True, on_delete=models.SET_NULL
    )


class Review(models.Model):
    """Настройки модели Отзывов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        """Метаданные модели отзывов."""

        ordering = ('pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return self.text


class Comments(models.Model):
    """Настройки модели Comment."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        """Метаданные модели комментариев."""

        default_related_name = 'comments'
        ordering = ('pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return self.text
