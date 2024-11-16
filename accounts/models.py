from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    username = models.CharField(_('username'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    age = models.PositiveIntegerField(_('age'), default=0, blank=True)  # age

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']