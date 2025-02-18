from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from .forms import RegisterForm, LoginForm
from .models import Register
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
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
    
    if User.objects.filter(email=email).exists():
      messages.error(self.request, "This registered email is already in use")
      return super().form_invalid(form)

    try:
      user = User.objects.create_user(username=email, email=email, password=password)
      Register.objects.create(user=user, date_of_birth=date_of_birth, image=image, phone=phone) #salva automaticamente no banco de dados por conta do metodo (create)
      messages.success(self.request, "Registration completed")
      return super().form_valid(form)
    except Exception as e:
      messages.error(self.request, f"Error {e}")
      return super().form_invalid(form)
  
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/account/'

    def form_valid(self, form):
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']

      user = authenticate(username=email, password=password)

      if user:
        login(self.request, user)
        messages.success(self.request, "Authenticated")
      else:
        messages.error(self.request, "Invalid credentials")
      return super().form_valid(form)
      


class AccountView(View):
  template_name = 'account.html'

  def get(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('login')
    return render(request, self.template_name)

  def post(self,request, *args, **kwargs):
    if 'delete_user' in request.POST:
      user = request.user
      user.delete()
      logout(request)
      messages.success(request, "Account deleted")
      return redirect('login')
    return redirect('index')

class LogoutView(View):
  def post(self, request):
    logout(request)
    return redirect('login')
       
       
    






