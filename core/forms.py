from django import forms
# from .models import Cadastro
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User

class CadastroForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    senha = forms.CharField(widget=forms.PasswordInput)

# class CadastroForm(forms.ModelForm):
#   senha = forms.CharField(widget=forms.PasswordInput)
#   data_nascimento = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         input_formats=['%Y-%m-%d']
#   )
#   class Meta:
#     model = Cadastro
#     fields = ['nome','email', 'data_nascimento', 'imagem', 'telefone', 'senha']
  
#   def save(self, commit=True):
#         # Cria o usuário usando o modelo User
#         user = User.objects.create_user(
#             username=self.cleaned_data['nome'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['senha'],
#         )

#         if commit:
#             user.save()

#         #O User, por sua vez, possui os atributos username, email, password, enquanto o Cadastro possui todos os atributos definidos no modelo Cadastro, além de ter um relacionamento com o User
#         cadastro = super().save(commit=False) #Instacia o objeto cadastro 
#         cadastro.user = user #Associa

#         if commit:
#             cadastro.save()

#         return cadastro

# class LoginForm(AuthenticationForm):
#   email = forms.EmailField(max_length=200)
#   senha = forms.CharField(widget=forms.PasswordInput)