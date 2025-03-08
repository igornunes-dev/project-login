from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Register
        fields = ['username','email', 'image']

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    enable_mfa = forms.BooleanField(required=False, label='Ativar MFA', initial=False)

class OTPForm(forms.Form):
    otp_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))

