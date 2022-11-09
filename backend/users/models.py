from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom user manager."""

    def create_user(self, username, password, **kwargs):
        """Creating a regular user."""
        user = self.model(
            username=username,
            password=password,
            **kwargs
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        """Creating a superuser."""
        user = self.model(
            username=username,
            password=password,
            **kwargs
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
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
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'
