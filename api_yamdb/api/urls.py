from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ReviewsViewSet, CommentsViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet)

urlpatterns = {
    path('v1/', include(router.urls))
}
