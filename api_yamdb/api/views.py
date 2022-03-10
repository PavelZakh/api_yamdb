from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from reviews.models import Reviews, Comments
from .serializers import ReviewsSerializer, CommentsSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """View Set for Reviews."""
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    # permission_classes =

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs["title_id"])


class CommentsViewSet(viewsets.ModelViewSet):
    """View Set for Comments."""
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    # permission_classes =

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Reviews, id=review_id)
        queryset = Comments.objects.filter(review_id__exact=review_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs["title_id"],
                        review_id=self.kwargs["review_id"])
