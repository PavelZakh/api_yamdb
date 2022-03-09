from django.db.models import Avg
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Categories, Genres, Titles
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleCreateSerializer, TitleListSerializer)


class TitlesViewSet(ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategorySerializer
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all().order_by('id')
    serializer_class = GenreSerializer
    search_fields = ['name']
    lookup_field = 'slug'
