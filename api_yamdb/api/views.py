from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Reviews, Comments
from .serializers import ReviewsSerializer, CommentsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
