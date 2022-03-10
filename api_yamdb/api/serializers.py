from rest_framework import serializers

from reviews.models import Reviews, Comments


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = '__all__'
        exclude = ('title_id',)
        model = Reviews

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
    author = serializers.StringRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
