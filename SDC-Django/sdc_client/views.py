from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'landing/home.html')

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def auth(request):
    return render(request, 'login/auth.html')

def feed(request):
    return render(request, 'posts/feed.html')

def create_post(request):
    return render(request, 'posts/create_post.html')