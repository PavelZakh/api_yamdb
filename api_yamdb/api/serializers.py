from rest_framework import serializers

from reviews.models import Reviews, Comments


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
