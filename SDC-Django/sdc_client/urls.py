# SDC-Django/sdc_client/urls.py

from django.urls import path
from . import views

# Importaciones de Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Vistas de páginas
    path('', views.home, name='home'),
    path('login-page/', views.login, name='login'), # Página de 'primer login'
    path('register/', views.register, name='register'),
    path('auth/', views.auth, name='auth'), # Página de 'auth' (formulario)
    
    # Feeds (requerirán protección JWT en el futuro)
    path('create_post/', views.create_post, name='create_post'),
    path('donee_feed', views.donee_feed, name='donee_feed'),
    path('donor_feed', views.donor_feed, name='donor_feed'),
    path('institution_feed', views.institution_feed, name='institution_feed'),

    # --- API Endpoints para Autenticación ---
    
    # 1. Tu vista de Login personalizada
    # La plantilla 'auth.html' debe enviar su POST a esta URL
    path('api/login/', views.api_login_view, name='api_login'), 
    
    # 2. Endpoints de Simple JWT (para refrescar tokens)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]