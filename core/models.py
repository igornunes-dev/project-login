from django.db import models
from django.contrib.auth.models import AbstractUser
from stdimage.models import StdImageField
from django.contrib.auth.models import User
from django.conf import settings

class Register(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

class CustomUser(AbstractUser):
  mfa_secret = models.CharField(max_length=32, blank=True, null=True)
