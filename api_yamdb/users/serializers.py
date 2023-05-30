import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError('Некорректный адрес электронной почты.')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с такой электронной почтой уже зарегистрирован.')
        if len(value) > 100:
            raise serializers.ValidationError('Длина адреса электронной почты превышает максимально допустимое значение (100 символов).')
        return value

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError('Имя пользователя не может быть пустой строкой.')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже зарегистрирован.')
        if len(value) > 150:
            raise serializers.ValidationError('Длина имени пользователя превышает максимально допустимое значение (150 символов).')
        if not value.isalnum():
            raise serializers.ValidationError('Имя пользователя может содержать только буквы и цифры.')
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя пользователя "me" недопустимо.')
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as v:
            raise serializers.ValidationError(v.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email', ''),
            username=validated_data.get('username', ''),
            password=validated_data.get('password', '')
        )
        return user

class ActivateUserSerializer(TokenObtainPairSerializer):
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = self.context['view'].kwargs['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('Указанный пользователь не найден.')

        if not user.is_active:
            raise serializers.ValidationError('Учетная запись пользователя не активирована.')

        if user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError('Неправильный код подтверждения.')

        attrs['user'] = user
        return attrs

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        return token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',)
        read_only_fields = ('id',)

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError(_('Некорректный адрес электронной почты.'))
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Пользователь с такой электронной почтой уже зарегистрирован.'))
        if len(value) > 100:
            raise serializers.ValidationError(_('Длина адреса электронной почты превышает максимально допустимое значение (100 символов).'))
        return value

    def validate_username(self, value):
        if not value.strip():
            raise serializers.ValidationError(_('Имя пользователя не может быть пустой строкой.'))
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(_('Пользователь с таким именем уже зарегистрирован.'))
        if len(value) > 150:
            raise serializers.ValidationError(_('Длина имени пользователя превышает максимально допустимое значение (150 символов).'))
        if not value.isalnum():
            raise serializers.ValidationError(_('Имя пользователя может содержать только буквы и цифры.'))
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username')
        )
        return user


class TokenObtainSerializer(TokenObtainPairSerializer):
    confirmation_code = serializers.CharField(max_length=100, write_only=True)

    def validate_confirmation_code(self, value):
        if len(value) != 6 or not value.isnumeric():
            raise serializers.ValidationError('Код подтверждения должен состоять из 6 цифр.')
        return value

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'first_name', 'last_name', 'bio']
        extra_kwargs = {'password': {'write_only': True}}


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'first_name', 'last_name', 'bio')

    def validate_email(self, value):
        # Проверка валидности email-адреса
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError('Некорректный формат email-адреса.')
        return value

    def validate_first_name(self, value):
        # Проверка максимальной длины имени
        if len(value) > 30:
            raise serializers.ValidationError('Имя должно содержать не более 30 символов.')
        return value

    def validate_last_name(self, value):
        # Проверка максимальной длины фамилии
        if len(value) > 30:
            raise serializers.ValidationError('Фамилия должна содержать не более 30 символов.')
        return value

    def validate_bio(self, value):
        # Проверка максимальной длины описания
        if len(value) > 500:
            raise serializers.ValidationError('Описание должно содержать не более 500 символов.')
        return value

    def update(self, instance, validated_data):
        role = validated_data.get('role')
        if role and not self.context['request'].user.is_superuser:
            raise serializers.ValidationError('Недостаточно прав для смены роли.')
        return super().update(instance, validated_data)