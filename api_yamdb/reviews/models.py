from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


ROLES = (
    ('user', 'аутентифицированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class Categories(models.Model):
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

    def __str__(self):
        return self.name


class Genres(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=256, verbose_name='genre name',
                            unique=True)
    slug = models.SlugField(unique=True, verbose_name='short link')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256, verbose_name='title name')
    year = models.IntegerField(verbose_name='year', null=True,)
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='description')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL,
                                 null=True, related_name="titles")
    genre = models.ManyToManyField(Genres, blank=True, related_name="titles")

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='электронная почта'
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='фамилия'
    )
    bio = models.TextField(
        null=True,
        verbose_name='информация о пользователе'
    )
    role = models.CharField(
        max_length=15,
        choices=ROLES,
        default='user',
        verbose_name='пользовательская роль'
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Review publication date', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_follow'
            )
        ]

        ordering = ['pub_date']


class Comment(models.Model):
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
