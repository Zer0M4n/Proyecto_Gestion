from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PersonRegistrationForm, InstitutionRegistrationForm

# Create your views here.

def home(request):
    return render(request, 'landing/home.html')

def login(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def auth(request):
    return render(request, 'login/auth.html')

def create_post(request):
    return render(request, 'posts/create_post.html')

def donee_feed(request):
    return render(request, 'posts/donee_feed.html')

def donor_feed(request):
    return render(request, 'posts/donor_feed.html')

def institution_feed(request):
    return render(request, 'posts/institution_feed.html')

# Logica para la vista register

def register(request):
    person_form = PersonRegistrationForm()
    institution_form = InstitutionRegistrationForm()

    if request.method == 'POST':
        if 'person_curp' in request.POST: # Campo único del form de persona
            person_form = PersonRegistrationForm(request.POST)
            if person_form.is_valid():
                # --- Lógica para guardar el usuario ---
                # ¡IMPORTANTE! Tu models.py está vacío.
                # Necesitas un Modelo de Usuario para guardar estos datos.
                # Ejemplo con el User de Django (solo guarda algunos campos):
                data = person_form.cleaned_data
                try:
                    # user = User.objects.create_user(
                    #     username=data['person_email'], 
                    #     email=data['person_email'],
                    #     password=data['person_password'],
                    #     first_name=data['person_first_name'],
                    #     last_name=data['person_first_surname']
                    # )
                    # Aquí deberías guardar el resto de datos (CURP, teléfono, tipo)
                    # en un modelo "Perfil" ligado al usuario.
                    
                    messages.success(request, '¡Registro de persona exitoso!')

                    # Redirigir según el tipo de usuario
                    if data['user_type'] == 'donee':
                        return redirect('donee_feed')
                    else:
                        return redirect('donor_feed')
                
                except Exception as e:
                    messages.error(request, f'Error al crear el usuario: {e}')

        elif 'institution_rfc' in request.POST: # Campo único del form de institución
            institution_form = InstitutionRegistrationForm(request.POST)
            if institution_form.is_valid():
                # --- Lógica para guardar la institución ---
                # data = institution_form.cleaned_data
                # user = User.objects.create_user(...)
                # institution_profile = InstitutionProfile.objects.create(user=user, rfc=data['institution_rfc'], ...)
                
                try:
                    # user = User.objects.create_user(
                    #     username=data['person_email'], 
                    #     email=data['person_email'],
                    #     password=data['person_password'],
                    #     first_name=data['person_first_name'],
                    #     last_name=data['person_first_surname']
                    # )
                    # Aquí deberías guardar el resto de datos (CURP, teléfono, tipo)
                    # en un modelo "Perfil" ligado al usuario.
                    
                    messages.success(request, '¡Registro de persona exitoso!')
                    return redirect('institution_feed')

                except Exception as e:
                    messages.error(request, f'Error al crear el usuario: {e}')

    # Si el método no es POST o los formularios no son válidos,
    # se renderiza la página con los formularios (y sus errores, si los hay)
    context = {
        'person_form': person_form,
        'institution_form': institution_form,
    }
    return render(request, 'login/register.html', context)