from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256,
                            verbose_name='category name',
                            unique=True)
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='short link')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=256, verbose_name='genre name',
                            unique=True)
    slug = models.SlugField(unique=True, verbose_name='short link')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256, verbose_name='title name')
    year = models.IntegerField(verbose_name='year', null=True,
                               validators=[year_validator],)
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='description')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
    genre = models.ManyToManyField(Genre, blank=True, related_name='titles')

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Модель пользователя."""
    ORDINARY_USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (ORDINARY_USER, 'аутентифицированный пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        null=True,
        verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default=ORDINARY_USER,
        verbose_name='Пользовательская роль'
    )

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class Review(models.Model):
    """Модель отзывов на произведения."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1, 'Оценка должна быть больше 1!'),
                    MaxValueValidator(10, 'Оценка должна быть меньше 10!')]
    )
    pub_date = models.DateTimeField(
        'Review publication date', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев на отзывы."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Comment publication date', auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
