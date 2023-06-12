from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    ADMIN = 'admin', 'Administrator'
    MODERATOR = 'moderator', 'Moderator'
    USER = 'user', 'User'


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.CharField(
        max_length=300,
        blank=True,
    )
    role = models.CharField(
        choices=Role.choices,
        default=Role.USER,
        max_length=10,
    )

    @property
    def is_user(self) -> bool:
        return self.role == Role.USER

    @property
    def is_moderator(self) -> bool:
        return self.role == Role.MODERATOR

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN or self.is_superuser

    class Meta:
        ordering = ('username',)
        default_related_name = 'user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def str(self) -> str:
        return self.username
