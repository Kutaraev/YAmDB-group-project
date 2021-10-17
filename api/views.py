from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import TitleFilter
from .mixins import CLDViewSet
from .models import Category, Genre, Review, Title
from .permissions import IsOwnerOrReadOnly, IsSuperUser, IsSuperUserOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer, TitleSerializer,
                          TitlesListSerializer, TokenObtainSerializer,
                          UserRegistrationSerializer, UserSerializer)

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsSuperUser,)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            serializer_class=UserSerializer)
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TokenObtainView(CreateAPIView):
    serializer_class = TokenObtainSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CLDViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = {SearchFilter}
    search_fields = ['name']


class GenresViewSet(CLDViewSet):
    serializer_class = GenresSerializer
    queryset = Genre.objects.all()
    lookup_url_kwarg = 'slug'
    lookup_field = 'slug'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    lookup_url_kwarg = 'titles_id'
    permission_classes = (IsSuperUserOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesListSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)

        serializer.save(
            author=user,
            title=get_object_or_404(
                Title, pk=self.kwargs.get('title_id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer.save(
            author=user,
            review=get_object_or_404(
                Review, pk=self.kwargs.get('review_id'))
        )
