from django.contrib.auth.models import AbstractUser
from django.db import models


ROLES = (
    ('user', 'аутентифицированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='имя пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=True,
        verbose_name='электронная почта',
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


class Reviews(models.Model):
    title_id = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='review'
    )
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Review publication date', auto_now_add=True
    )


class Comments(models.Model):
    title_id = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='comments'
    )
    review_id = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Comment publication date', auto_now_add=True
    )
