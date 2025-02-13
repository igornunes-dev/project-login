from django.urls import path, include
from .views import IndexView, LoginView, AccountView
from django.conf import settings
from django.conf.urls.static import static
#oferece views prontas - LogoutView é uma
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)