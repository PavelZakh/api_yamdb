from rest_framework import serializers

from reviews.models import Reviews, Comments


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
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
    class Meta:
        fields = '__all__'
        model = Comments
