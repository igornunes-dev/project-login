from django.urls import path, include
from .views import IndexView, LoginView, AccountView, LogoutView, ProfileView, VerificationView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verification/', VerificationView.as_view(), name='verification')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)