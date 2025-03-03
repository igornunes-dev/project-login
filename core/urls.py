from django.urls import path
from .views import IndexView, LoginView, AccountView, LogoutView, ProfileView, VerificationView, CustomPasswordResetView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('2FA/', ProfileView.as_view(), name='2FA'),
    path('verification/', VerificationView.as_view(), name='verification'),
    path('reset_password/', CustomPasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)