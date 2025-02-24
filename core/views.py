from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, OTPForm
from .models import Register
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
import pyotp
import qrcode
import io
import base64
from django.utils.timezone import localtime

CustomUser = get_user_model()

class TwoFactorAuth:
    """Classe para lidar com a verificação de 2FA."""

    def __init__(self, user):
        self.user = user
        self.totp = pyotp.TOTP(user.mfa_secret)
    
    def verify(self, otp):
        """Verifica o código OTP e habilita a autenticação 2FA se for válido."""
        if self.totp.verify(otp):
            self.user.mfa_enable = True
            self.user.save()
            return True
        return False

class ProfileView(FormView):
    template_name = '2FA.html'
    form_class = OTPForm

    def _generate_qr_code(self, user):
        """Método auxiliar para gerar o QR Code baseado no mfa_secret do usuário"""

        if not user.mfa_secret:
            user.mfa_secret = pyotp.random_base32()
            user.save()
            
        otp = pyotp.TOTP(user.mfa_secret).provisioning_uri(
            name=user.email,
            issuer_name="Login"
        )
        qr = qrcode.make(otp)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        qr_code_data = self._generate_qr_code(user)
        context['qrcode'] = f"data:image/png;base64,{qr_code_data}"
        context['form'] = self.get_form()

        return context

    def form_valid(self, form):
        """Processa o envio do código OTP e valida o código inserido"""
        user = self.request.user
        otp_code = form.cleaned_data['otp_code']
        
        # Verifica o código OTP
        if pyotp.TOTP(user.mfa_secret).verify(otp_code):
            messages.success(self.request, "Código OTP verificado com sucesso!")
            return redirect("account")  # Redireciona para a página da conta
        else:
            messages.error(self.request, "Código OTP inválido!")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Se o formulário for inválido ou o OTP for inválido, retorna ao perfil"""
        user = self.request.user
        qr_code_data = self._generate_qr_code(user)  # Regerar QR Code
        return self.render_to_response(self.get_context_data(
            form=form,
            qrcode=f"data:image/png;base64,{qr_code_data}"
        ))

class VerificationView(View):
    def post(self, request, *args, **kwargs):
        """ Verifica o código OTP enviado pelo usuário. """
        user_id = request.session.get("user_id")
        user = CustomUser.objects.filter(id=user_id).first()

        if not user:
            messages.error(request, "Usuário não encontrado")
            return redirect("login")

        otp_code = request.POST.get('otp_code')
        if not otp_code:
            messages.error(request, "Código OTP não enviado.")
            return redirect("2FA")

        # Verificação do código OTP
        if pyotp.TOTP(user.mfa_secret).verify(otp_code):
            # Login do usuário
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("account")  # Redireciona para a página de conta

        messages.error(request, "Código OTP inválido!")
        return redirect("2FA") 
    

class IndexView(FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        date_of_birth = form.cleaned_data['date_of_birth']
        phone = form.cleaned_data['phone']
        image = form.cleaned_data['image']
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Este email já está em uso.")
            return super().form_invalid(form)
        
        try:
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
            Register.objects.create(user=user, date_of_birth=date_of_birth, image=image, phone=phone)
            messages.success(self.request, "Registro concluído com sucesso.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Erro: {e}")
            return super().form_invalid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/account/'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        enable_mfa = form.cleaned_data.get('enable_mfa', False)  # Verifica se o usuário marcou a opção de ativar MFA

        user = authenticate(username=email, password=password)

        if user:
            login(self.request, user)

            if enable_mfa:  # Se o usuário marcou para ativar MFA
                user.mfa_enable = True
                user.mfa_secret = pyotp.random_base32()  # Gera um novo segredo para MFA
                user.save()

                self.request.session['user_id'] = user.id  # Armazena o ID do usuário na sessão
                return redirect('2FA')  # Redireciona para a página de perfil onde o usuário configurará o MFA

            if user.mfa_enable:  # Se o MFA já estiver ativado para o usuário
                self.request.session['user_id'] = user.id
                return redirect('verification')  # Redireciona para a página de verificação do OTP
            messages.success(self.request, "Autenticado com sucesso.")
            return redirect('account')  # Redireciona diretamente para a conta se MFA não for necessário
        else:
            messages.error(self.request, "Credenciais inválidas.")
        return super().form_valid(form)

#### AQUI VERIFICARRRR
class AccountView(View):
    template_name = 'account.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {
            'user_last_login': localtime(request.user.last_login),
            'user_date_joined': localtime(request.user.date_joined),
        }
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'delete_user' in request.POST:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Conta excluída com sucesso.")
            return redirect('login')
        return redirect('index')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')