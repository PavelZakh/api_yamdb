from rest_framework import viewsets

from reviews.models import Reviews, Comments
from .serializers import ReviewsSerializer, CommentsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = CommentsSerializer
