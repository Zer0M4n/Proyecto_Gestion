from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('auth/', views.auth, name='auth'),
    path('create_post/', views.create_post, name='create_post'),
    path('donee_feed', views.donee_feed, name='donee_feed'),
    path('donor_feed', views.donor_feed, name='donor_feed'),
    path('institution_feed', views.institution_feed, name='institution_feed'),
]