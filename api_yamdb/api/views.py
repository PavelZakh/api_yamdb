from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Reviews, Comments
from .serializers import ReviewsSerializer, CommentsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs["title_id"])


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs["title_id"],
                        review_id=self.kwargs["review_id"])
