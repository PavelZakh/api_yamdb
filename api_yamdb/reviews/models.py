from django.db import models


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


class Titles(models.Model):
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
        verbose_name = ('title')
        verbose_name_plural = ('titles')

    def __str__(self):
        return self.name
