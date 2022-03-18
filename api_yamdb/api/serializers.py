from rest_framework import serializers
from reviews.models import User
from reviews.models import Reviews, Comments
from reviews.models import Categories, Genres, Titles


class EmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        model = Reviews
        read_only_fields = ('author', 'pub_date')
    '''
    def validate(self, data):
        if not isinstance(data['score'], int):
            raise serializers.ValidationError(
                "Enter integer score!"
            )
        if data['score'] not in range(11):
            raise serializers.ValidationError(
                "Enter score between 0 and 10!"
            )
        return data
'''


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('title',)
        model = Comments
        read_only_fields = ('title', 'review', 'pub_date')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категорий"""

    class Meta:
        model = Categories
        exclude = ('id',)
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанров"""

    class Meta:
        model = Genres
        exclude = ('id',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для POST запросов модели Title"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )

    class Meta:
        model = Titles
        fields = '__all__'


class TitleGetSerializer(serializers.ModelSerializer):
    """Серилализатор для GET запросов модели Title"""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Titles
