from django.db import models
# from django.contrib.auth.hashers import make_password
from stdimage.models import StdImageField
from django.contrib.auth.models import User
# # Create your models here.

class Register(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  date_of_birth = models.DateField('Date of birth')
  image = StdImageField('Image', upload_to='photo', variations={'thumb': (420, 420)}, null=True, blank=True)
  phone = models.CharField('Phone', max_length=20)

#   #sobrescrevendo
#   def save(self, *args, **kwargs):
#     #verifica se a senha esta vazia e se começa com pbkdf2_sha256
#     if self.senha and not self.senha.startswith('pbkdf2_sha256'):
#       #criptografa
#       self.senha = make_password(self.senha)
#     # Chama o método save da superclasse para salvar no banco de dados
#     super(Cadastro, self).save(*args, **kwargs)

#   def __str__(self):
#     return self.nome