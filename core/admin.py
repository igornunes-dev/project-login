from django.contrib import admin
from .models import Cadastro
# Register your models here.

@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
  list_display = ('user', 'email', 'data_nascimento', 'telefone', 'senha')