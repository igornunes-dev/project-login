from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Register

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']
    
    # Definir campos adicionais
   

# Registra o modelo CustomUser com a classe CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)