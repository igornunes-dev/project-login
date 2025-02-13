from django.db import models
from django.contrib.auth.hashers import make_password
from stdimage.models import StdImageField
from django.contrib.auth.models import User
# Create your models here.

class Cadastro(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  nome = models.CharField('Nome', max_length=200, null=True, blank=True)
  email = models.CharField('Email', max_length=200)
  data_nascimento = models.DateField('Data de Nascimento')
  imagem = StdImageField('Imagem', upload_to='media/foto', variations={'thumb': (420, 420)}, null=True, blank=True)
  telefone = models.CharField('Telefone', max_length=20)
  senha = models.CharField('Senha', max_length=128)

  #sobrescrevendo
  def save(self, *args, **kwargs):
    #verifica se a senha esta vazia e se começa com pbkdf2_sha256
    if self.senha and not self.senha.startswith('pbkdf2_sha256'):
      #criptografa
      self.senha = make_password(self.senha)
    # Chama o método save da superclasse para salvar no banco de dados
    super(Cadastro, self).save(*args, **kwargs)

  def __str__(self):
    return self.nome