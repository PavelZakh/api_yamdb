from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, get_confirmation_code, get_jwt_token

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/mail/', get_confirmation_code),
    path('v1/auth/token/', get_jwt_token)
]
