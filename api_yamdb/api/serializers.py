from rest_framework import serializers

from api.models import Category, Genre, Title


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий"""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанров"""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов модели Title"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
    )

    class Meta:
        model = Title
        fields = ('__all__')


class TitleGetSerializer(serializers.ModelSerializer):
    """Серилализатор для GET запросов модели Title"""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
