from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('auth/', views.auth, name='auth'),
    path('feed/', views.feed, name='feed'),
    path('create_post/', views.create_post, name='create_post'),
]