from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from reviews.models import Category, Genre, Title
from .filter import TitlesFilter
from rest_framework import mixins, viewsets, filters
from .permissions import IsAdminOrReadOnly, IsAdmin, IsAuthorOrReadOnly, IsAdminModeratorOwnerOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer, TitleGetSerializer,
                             TitlePostSerializer, ReviewsSerializer, CommentsSerializer)


class CategoryViewSet():
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryViewSet(ListCreateViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer
