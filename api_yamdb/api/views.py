from api_yamdb.settings import EMAIL_HOST_USER
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comments, Genres, Reviews, Titles, User

from api.permissions import IsAdminOrSuperUser, CommentReviewPermissios
from api.serializers import (CategoriesSerializer, CommentsSerializer,
                             ConfirmationCodeSerializer, EmailSerializer,
                             GenresSerializer, ReviewsSerializer,
                             TitleGetSerializer, TitlesSerializer,
                             UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    if email is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if username is not None:
        try:
            User.objects.create_user(username=username, email=email)
        except IntegrityError:
            return Response(
                {'Пользователь с таким username/email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    mail_subject = 'Код подтверждения на Yamdb.ru'
    send_mail(mail_subject, message, EMAIL_HOST_USER, [email])
    return Response(
        {f'На почту {email} был выслан ваш код подтверждения'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """API для модели пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewsViewSet(viewsets.ModelViewSet):
    """View Set for Reviews."""
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (CommentReviewPermissios,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title_id=self.kwargs["title_id"])


class CommentsViewSet(viewsets.ModelViewSet):
    """View Set for Comments."""
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (CommentReviewPermissios,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Reviews, id=review_id)
        queryset = Comments.objects.filter(review__exact=review)
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Reviews, id=self.kwargs.get("review_id"))
        title = get_object_or_404(Titles, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user,
                        title=title,
                        review=review,
                        )


class TitlesViewSet(ModelViewSet):
    queryset = Titles.objects.annotate(
        rating=Avg('review__score')).order_by('id')

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitlesSerializer
        return TitleGetSerializer


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    search_fields = ['name']
    lookup_field = 'slug'
