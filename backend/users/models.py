from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from config import config_messages as msg


class CustomUserManager(BaseUserManager):
    """Custom user manager."""

    def _create_user(self, email, username, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop('is_superuser', False)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, username, password, **kwargs):
        """Creating a user."""
        return self._create_user(email, username, password, **kwargs)

    def create_superuser(self, email, username, password, **kwargs):
        """Creating a superuser."""
        return self._create_user(
            email=email, username=username, password=password,
            is_staff=True, is_superuser=True, **kwargs
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Stores a single custom user entry.
    Required fields:
    - email, username, first_name, last_name.
    """
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email address'
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Username'
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='First name'
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='Last name'
    )

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=msg.IS_ACTIVE
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text=msg.IS_STAFF
    )
    is_subscribed = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def is_admin(self) -> bool:
        """Declare that it can be accessed like it's a regular property."""
        return self.is_superuser

    def __str__(self) -> str:
        """Return string representation of the object."""
        return f'{self.username}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'


class Follow(models.Model):
    """
    Stores a single follow entry, related to:
    :model:`user.User`,
    :model:`author.User`.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]
        db_table = 'follows'
