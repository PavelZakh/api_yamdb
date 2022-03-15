from rest_framework import serializers
from reviews.models import User
from reviews.models import Reviews, Comments

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
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
        exclude = ('title_id',)
        model = Reviews
        read_only_fields = ('author', 'pub_date')

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


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('title_id',)
        model = Comments
        read_only_fields = ('title_id', 'review_id', 'pub_date')
