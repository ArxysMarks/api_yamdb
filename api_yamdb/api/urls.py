from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, GenresViewSet, TitlesViewSet,
                       ReviewViewSet, CommentViewSet)

router = routers.DefaultRouter()


router.register('titles', TitlesViewSet)
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='category')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
