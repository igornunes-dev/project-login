from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
# from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from .forms import CadastroForm, LoginForm
# from .models import Cadastro
from django.urls import reverse_lazy
from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView
# Create your views here.


class IndexView(FormView):
  template_name = 'cadastro.html'
  form_class = CadastroForm
  success_url = reverse_lazy('login')

  def form_valid(self, form):
    username = form.cleaned_data['email']
    email = form.cleaned_data['email']
    senha = form.cleaned_data['senha']
    
    user_exist = User.objects.filter(email=email)

    if (self, user_exist):
      messages.error(self.request, "Ja existe")

    user = User.objects.create_user(username=email, email=email, password=senha)
    user.save()

    return super().form_valid(form)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/account/'

    def form_valid(self, form):
      email = form.cleaned_data['email']
      senha = form.cleaned_data['senha']

      user = authenticate(username=email, password=senha)

      if user:
        login(self.request, user)
        messages.success(self.request, "Autenticado")
      return super().form_valid(form)
      

class AccountView(TemplateView):
  template_name = 'account.html'

class LogoutView(View):
  def post(self, request):
    logout(request)
    return redirect('login')
       
       
    






