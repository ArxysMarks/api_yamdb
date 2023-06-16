from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('"me" username is not allowed.')
        return value

    def validate(self, data):
        if User.objects.filter(
            email=data['email'],
            username=data['username'],
        ).exists():
            return data
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Данный email уже занят.')
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Данное имя уже занято.')
        return data
