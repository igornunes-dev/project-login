from django import forms
from .models import Register
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Register
        fields = ['username','email','date_of_birth', 'image', 'phone']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)