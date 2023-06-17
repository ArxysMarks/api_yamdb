from rest_framework import mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAdminOrReadOnly,)
    pass
