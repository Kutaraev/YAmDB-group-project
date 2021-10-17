from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet, TokenObtainView,
                    UserRegistrationView, UsersViewSet)

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)

router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainView.as_view()),
    path('v1/auth/email/', UserRegistrationView.as_view()),
]
