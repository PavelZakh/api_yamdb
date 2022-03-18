from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, get_confirmation_code, get_jwt_token

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitlesViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitlesViewSet, basename='Title')
router.register('genres', GenreViewSet, basename='Genre')
router.register('categories', CategoryViewSet, basename='Category')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='Title')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentsViewSet, basename='Comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', get_confirmation_code),
    path('v1/auth/token/', get_jwt_token)
]
