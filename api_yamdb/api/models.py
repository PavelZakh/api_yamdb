from django.db import models


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(max_length=256,
                            verbose_name='Категория',
                            unique=True)
    slug = models.SlugField(unique=True,
                            max_length=50,
                            verbose_name='Краткая ссылка категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(max_length=256, verbose_name='Жанр', unique=True)
    slug = models.SlugField(unique=True, verbose_name='Краткая ссылка жанра')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=256, verbose_name='Произведение')
    year = models.IntegerField(verbose_name='Год', null=True,)
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name="titles")
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")

    class Meta:
        verbose_name = ('Заголовок')
        verbose_name_plural = ('Заголовки')

    def __str__(self):
        return self.name
