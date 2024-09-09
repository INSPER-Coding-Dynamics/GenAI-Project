from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='AiChatApp/login.html'), name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('', views.home, name='home'),
]