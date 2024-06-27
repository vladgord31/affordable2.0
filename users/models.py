from django.db import models
from django.contrib.auth.models import AbstractUser
from main.models import Seat
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    image = models.ImageField(upload_to="users_image", blank=True, null=True, verbose_name="Аватарка:")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
