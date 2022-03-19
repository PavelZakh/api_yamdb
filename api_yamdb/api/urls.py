from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitlesViewSet, UserViewSet,
                    get_confirmation_code, get_jwt_token)

app_name = 'api'

rout = r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitlesViewSet, basename='Title')
router.register('genres', GenreViewSet, basename='Genre')
router.register('categories', CategoryViewSet, basename='Category')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='Title')
router.register(rout, CommentsViewSet, basename='Comment')

urlpatterns = [
    path('v1/', include(router.urls), name='api_v1'),
    path('v1/auth/signup/', get_confirmation_code, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='token')
]
