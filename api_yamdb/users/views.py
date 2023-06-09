from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (GetTokenSerializer, SignUpSerializer,
                               UserSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.validated_data['username'])
    if user.is_confirmation_code_valid(serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Confirmation code is invalid.'},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'me':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения для завершения регистрации:',
        confirmation_code,
        'ya@mdb.com',
        [user.email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)
