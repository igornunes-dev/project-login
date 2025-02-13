from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from .forms import CadastroForm
from .models import Cadastro
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.


class IndexView(FormView):
  template_name = 'cadastro.html'
  form_class = CadastroForm
  model = Cadastro
  success_url = reverse_lazy("login")

  def form_valid(self, form):
    form.save()
    # Ele chama o comportamento padrão de sucesso do formulário, que valida, salva os dados e redireciona o usuário para a URL de sucesso.
    return super().form_valid(form)



class LoginView(LoginView):
  template_name = 'login.html'

  def form_valid(self, form):
    messages.success(self.request, "Login feito com sucesso")
    return super().form_valid(form)
  
  def form_invalid(self, form):
    messages.error(self.request, "Usuário ou senha invalidos")
    return super().form_invalid(form)
  
class AccountView(LoginRequiredMixin, DetailView):
  model = Cadastro
  template_name = "account.html"
  context_object_name = "user"
  login_url = "/login/"

  #substitue a logica padrão de pegar o user baseado em pk por uma que simplesmente pega o usuario
  def get_object(self, queryset=None):
    return self.request.user
  
  def post(self, request, *args, **kwargs):
    print('deletado')
    if 'delete_user' in request.POST:
      user = request.user
      user.delete()
      return redirect('login')
    return super().post(request, *args, **kwargs)
