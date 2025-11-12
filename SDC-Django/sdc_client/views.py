# SDC-Django/sdc_client/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction # Para asegurar que User y Perfil se creen juntos
from django.contrib.auth import authenticate, login # Para Login
from django.http import JsonResponse
import json

# Importa tus formularios
from .forms import PersonRegistrationForm, InstitutionRegistrationForm
# Importa tus nuevos modelos
from .models import CustomUser, Donee, Donor, Institution

# Importaciones para JWT y Vistas de API (para el login)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


# --- Vistas de Páginas (Frontend) ---

def home(request):
    return render(request, 'landing/home.html')

def login(request):
    # Esta vista ahora solo muestra la página 'login.html'
    return render(request, 'login/login.html')

def auth(request):
    # Esta vista ahora solo muestra la página 'auth.html'
    return render(request, 'login/auth.html')

def create_post(request):
    return render(request, 'posts/create_post.html')

def donee_feed(request):
    return render(request, 'posts/donee_feed.html')

def donor_feed(request):
    return render(request, 'posts/donor_feed.html')

def institution_feed(request):
    return render(request, 'posts/institution_feed.html')


# --- Lógica de Registro (Backend) ---

def register(request):
    person_form = PersonRegistrationForm()
    institution_form = InstitutionRegistrationForm()

    if request.method == 'POST':
        # --- Lógica de Registro de Persona ---
        if 'person_curp' in request.POST:
            person_form = PersonRegistrationForm(request.POST)
            if person_form.is_valid():
                data = person_form.cleaned_data
                
                # Usamos una transacción para asegurar que ambos se creen
                try:
                    with transaction.atomic():
                        # 1. Crear el CustomUser
                        # Usamos nuestro CustomUserManager (create_user)
                        # Esto se encarga de HASHEAR la contraseña
                        user = CustomUser.objects.create_user(
                            email=data['person_email'],
                            phone=data['person_phone'],
                            password=data['person_password']
                        )
                        
                        # 2. Crear el Perfil (Donee o Donor)
                        profile_data = {
                            'user': user,
                            'first_name': data['person_first_name'],
                            'middle_name': data['person_middle_name'],
                            'first_surname': data['person_first_surname'],
                            'second_surname': data['person_second_surname'],
                            'curp': data['person_curp'],
                            'city': data['person_city'],
                            'state': data['person_state']
                        }

                        if data['user_type'] == 'donee':
                            Donee.objects.create(**profile_data)
                            redirect_url = 'donee_feed'
                        else: # 'donor'
                            Donor.objects.create(**profile_data)
                            redirect_url = 'donor_feed'

                    messages.success(request, '¡Registro exitoso! Por favor, inicia sesión.')
                    return redirect('auth') # Redirigir a la página de login

                except Exception as e:
                    # Captura errores (ej. email duplicado)
                    messages.error(request, f'Error al crear el usuario: {e}')

        # --- Lógica de Registro de Institución ---
        elif 'institution_rfc' in request.POST:
            institution_form = InstitutionRegistrationForm(request.POST)
            if institution_form.is_valid():
                data = institution_form.cleaned_data

                try:
                    with transaction.atomic():
                        # 1. Crear el CustomUser para la institución
                        user = CustomUser.objects.create_user(
                            email=data['institution_email'],
                            # Tu schema no tiene 'phone' para institución
                            # Asumiremos un valor temporal o ajusta el modelo
                            phone=data['institution_rfc'], # Usar RFC como fono temporal
                            password=data['institution_password']
                        )
                        
                        # 2. Crear el Perfil de Institución
                        Institution.objects.create(
                            user=user,
                            name=data['institution_name'],
                            rfc=data['institution_rfc'],
                            city=data['institution_city'],
                            state=data['institution_state'],
                            address=data['institution_address']
                        )
                    
                    messages.success(request, '¡Registro de institución exitoso! Por favor, inicia sesión.')
                    return redirect('auth') # Redirigir a la página de login

                except Exception as e:
                    messages.error(request, f'Error al crear la institución: {e}')

    # Si es GET o el formulario no es válido, renderiza la página con los errores
    context = {
        'person_form': person_form,
        'institution_form': institution_form,
    }
    return render(request, 'login/register.html', context)


# --- Lógica de Login (Backend) con JWT ---
# Esta vista reemplazará tu antigua vista 'auth'
# Se convertirá en un endpoint de API que devuelve un token

@api_view(['POST']) # Solo acepta peticiones POST
@permission_classes([AllowAny]) # Cualquiera puede intentar iniciar sesión
def api_login_view(request):
    
    # Usamos request.data en lugar de request.POST para DRF
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Email y contraseña requeridos'}, status=400)

    # authenticate() usa nuestro CustomUser y maneja el hashing
    user = authenticate(request, email=email, password=password)

    if user is not None:
        # ¡Autenticación exitosa!
        # Generamos los tokens JWT
        refresh = RefreshToken.for_user(user)
        
        # Debemos determinar el tipo de usuario para la redirección en el frontend
        user_type = 'unknown'
        redirect_url = '/' # Default
        
        if hasattr(user, 'donor'):
            user_type = 'donor'
            redirect_url = '/donor_feed' # URL de 'donor_feed'
        elif hasattr(user, 'donee'):
            user_type = 'donee'
            redirect_url = '/donee_feed'
        elif hasattr(user, 'institution'):
            user_type = 'institution'
            redirect_url = '/institution_feed'
        
        # Devolvemos los tokens y la información del usuario
        return JsonResponse({
            'message': 'Login exitoso',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'user_type': user_type,
                'redirect_url': redirect_url
            }
        }, status=200)
    else:
        # Autenticación fallida
        return JsonResponse({'error': 'Credenciales inválidas'}, status=401)