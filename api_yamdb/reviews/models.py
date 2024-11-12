from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    role = models.CharField("роль", max_length=20, blank=True)


class Review(models.Model):
    """Настройки модели Отзывов."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(default=0)

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
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        """Метаданные модели комментариев."""

        default_related_name = 'comments'
        ordering = ('pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return self.text
