from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, OTPForm
from .models import Register
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import pyotp
import qrcode
import io
import base64
from django.utils.timezone import localtime

CustomUser = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        # Checks if the email is registered
        if not email or not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "No account found with this email.")
            return redirect("password_reset") 

        user = CustomUser.objects.get(email=email)
        domain = get_current_site(request).domain
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        context = {
            "email": user.email,
            "domain": domain,
            "site_name": get_current_site(request).name,
            "uid": uid,
            "user": user,
            "token": token,
            "protocol": "https" if request.is_secure() else "http",
        }

        # Renders the email body
        subject = render_to_string("registration/password_reset_subject.txt", context)
        subject = "".join(subject.splitlines())  # Removes line breaks from the subject
        body = render_to_string("registration/password_reset_email.html", context)

        # Sends the email with both text and HTML support
        email_message = EmailMultiAlternatives(
            subject,  # Subject
            body,     # Text email body
            'from_email@example.com',  # Sender
            [user.email]  # Recipient
        )

        # Attaches the HTML version of the email
        email_message.attach_alternative(body, "text/html")

        # Sends the email
        email_message.send()

        messages.success(request, "Password recovery email sent successfully. Check your inbox.")
        return redirect("password_reset_done")
    
class TwoFactorAuth:
    """Class to handle 2FA verification."""

    def __init__(self, user):
        self.user = user
        self.totp = pyotp.TOTP(user.mfa_secret)
    
    def verify(self, otp):
        """Verifies the OTP code and enables 2FA if valid."""
        if self.totp.verify(otp):
            self.user.save()
            return True
        return False

class ProfileView(FormView):
    template_name = '2FA.html'
    form_class = OTPForm

    def dispatch(self, request, *args, **kwargs):
        """Verifica se o usuário está autenticado antes de prosseguir com o processamento da requisição"""
        if not request.user.is_authenticated:
            print("REDIRECIONANDO PARA LOGIN")
            return redirect('login')  # Redireciona para o login se o usuário não estiver autenticado
        return super().dispatch(request, *args, **kwargs)

    def _generate_qr_code(self, user):
        """Helper method to generate the QR Code based on the user's mfa_secret"""

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
        """Processes OTP submission and validates the code"""
        user = self.request.user
        
        otp_code = form.cleaned_data['otp_code']    
        
        # Verifies the OTP code
        if pyotp.TOTP(user.mfa_secret).verify(otp_code):
            messages.success(self.request, "OTP code verified successfully!")
            return redirect("account")  # Redirects to the account page
        else:
            messages.error(self.request, "Invalid OTP code!")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """If the form is invalid or the OTP is invalid, returns to profile"""
        user = self.request.user
        
        qr_code_data = self._generate_qr_code(user)  # Regenerate QR Code
        return self.render_to_response(self.get_context_data(
            form=form,
            qrcode=f"data:image/png;base64,{qr_code_data}"
        ))

class VerificationView(View):
    def post(self, request, *args, **kwargs):
        """Verifies the OTP code submitted by the user."""
        user_id = self.request.session.get("user_id")
        user = CustomUser.objects.filter(id=user_id).first()

        if not user:
            messages.error(request, "User not found")
            return redirect("login")

        otp_code = request.POST.get('otp_code')
        if not otp_code:
            messages.error(request, "OTP code not sent.")
            return redirect("2FA")

        # Verifies the OTP code
        if pyotp.TOTP(user.mfa_secret).verify(otp_code):
            # Logs the user in
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("account")  # Redirects to account page

        messages.error(request, "Invalid OTP code!")
        return redirect("2FA") 
    

class IndexView(FormView):
    template_name = 'index.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        phone = form.cleaned_data['phone']
        image = form.cleaned_data['image']
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "This email is already in use.")
            return super().form_invalid(form)
        
        try:
            user = CustomUser.objects.create_user(username=email, email=email, password=password)
            Register.objects.create(user=user, image=image, phone=phone)
            messages.success(self.request, "Registration successful.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error: {e}")
            return super().form_invalid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/account/'  # Caso o login seja bem-sucedido, vai para a conta do usuário

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        enable_mfa = form.cleaned_data.get('enable_mfa', False)  # Verifica se o checkbox foi marcado

        user = authenticate(username=email, password=password)

        print(f"enable_mfa: {enable_mfa}")
        if user:
            # Se o checkbox de MFA estiver marcado, redireciona para 2FA
            if enable_mfa:
                # Gerar um segredo para o usuário se não tiver MFA habilitad
                login(self.request, user)
                self.request.session['user_id'] = user.id
                print("MFA ativado, redirecionando para 2FA.")
                return redirect('2FA') 

            # Se o MFA não estiver ativado, realiza o login normalmente
            print("Usuário autenticado, redirecionando para account.")
            print(f"Usuário autenticado: {user}")
            login(self.request, user)
            messages.success(self.request, "Authenticated successfully.")
            return redirect('account')  # Redireciona para a página da conta do usuário
        else:
            messages.error(self.request, "Invalid credentials.")

        return super().form_valid(form)


class AccountView(View):
    template_name = 'account.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'delete_user' in request.POST:
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, "Account successfully deleted.")
            return redirect('login')
        return redirect('index')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')
