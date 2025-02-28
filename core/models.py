from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password
from stdimage.models import StdImageField
from django.contrib.auth.models import User
from django.conf import settings
# # Create your models here.

class Register(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
  date_of_birth = models.DateField('Date of birth')
  image = StdImageField('Image', upload_to='photo', variations={'thumb': (420, 420)}, null=True, blank=True)
  phone = models.CharField('Phone', max_length=20)

class CustomUser(AbstractUser):
  mfa_secret = models.CharField(max_length=32, blank=True, null=True)
