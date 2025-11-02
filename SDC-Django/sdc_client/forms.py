import re
from django import forms
from django.core.exceptions import ValidationError

# --- Funciones de Validación Reutilizables ---

def validate_no_numbers(value):
    """Valida que el campo no contenga números."""
    if any(char.isdigit() for char in value):
        raise ValidationError('Este campo no puede contener números.')

def validate_phone(value):
    """Valida que el campo solo contenga números."""
    if not value.isdigit():
        raise ValidationError('El teléfono debe contener solo números.')

def validate_curp(value):
    """Valida el formato de CURP."""
    curp_regex = r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS){1}[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]{1}[0-9]{1}$'
    if not re.match(curp_regex, value.upper()):
        raise ValidationError('El formato del CURP no es válido.')

def validate_rfc(value):
    """Valida el formato de RFC."""
    rfc_regex = r'^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{3}$'
    if not re.match(rfc_regex, value.upper()):
        raise ValidationError('El formato del RFC no es válido.')

# --- Formularios de Registro ---

class PersonRegistrationForm(forms.Form):
    person_first_name = forms.CharField(label='Primer nombre', max_length=100, validators=[validate_no_numbers])
    person_middle_name = forms.CharField(label='Segundo nombre', max_length=100, required=False, validators=[validate_no_numbers])
    person_first_surname = forms.CharField(label='Primer apellido', max_length=100, validators=[validate_no_numbers])
    person_second_surname = forms.CharField(label='Segundo apellido', max_length=100, validators=[validate_no_numbers])
    person_curp = forms.CharField(label='CURP', max_length=18, validators=[validate_curp])
    person_city = forms.CharField(label='Ciudad', max_length=100)
    person_state = forms.CharField(label='Estado', max_length=100)
    person_email = forms.EmailField(label='Correo electrónico')
    person_phone = forms.CharField(label='Teléfono', max_length=15, validators=[validate_phone])
    person_password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirm_person_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    user_type = forms.ChoiceField(label='Tipo de usuario', choices=[('donee', 'Donatario'), ('donor', 'Donador')])

    def clean_person_email(self):
        """Valida que el email no esté ya en uso."""
        email = self.cleaned_data.get('person_email')
        # Aquí deberías importar tu modelo de Usuario (ej. User de auth)
        # from django.contrib.auth.models import User
        # if User.objects.filter(email=email).exists():
        #     raise ValidationError("Este correo electrónico ya está registrado.")
        # Como tu models.py está vacío, esta lógica está comentada.
        # ¡Descomenta y ajusta cuando tengas tu modelo de usuario!
        return email

    def clean(self):
        """Valida que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("person_password")
        confirm_password = cleaned_data.get("confirm_person_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_person_password', "Las contraseñas no coinciden.")
        
        # Validación de seguridad de contraseña
        if password:
            if len(password) < 8:
                self.add_error('person_password', 'La contraseña debe tener al menos 8 caracteres.')
            if not re.search(r'[A-Z]', password):
                self.add_error('person_password', 'La contraseña debe contener al menos una mayúscula.')
            if not re.search(r'[0-9]', password):
                self.add_error('person_password', 'La contraseña debe contener al menos un número.')
        
        return cleaned_data

class InstitutionRegistrationForm(forms.Form):
    institution_name = forms.CharField(label='Nombre de la institución', max_length=255)
    institution_rfc = forms.CharField(label='RFC', max_length=13, validators=[validate_rfc])
    institution_city = forms.CharField(label='Ciudad', max_length=100)
    institution_state = forms.CharField(label='Estado', max_length=100)
    institution_address = forms.CharField(label='Dirección', max_length=255)
    institution_email = forms.EmailField(label='Correo institucional')
    institution_password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    confirm_institution_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean_institution_email(self):
        """Valida que el email no esté ya en uso."""
        email = self.cleaned_data.get('institution_email')
        # Similar al otro form, aquí va tu lógica de validación de email existente
        return email

    def clean(self):
        """Valida que las contraseñas coincidan."""
        cleaned_data = super().clean()
        password = cleaned_data.get("institution_password")
        confirm_password = cleaned_data.get("confirm_institution_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_institution_password', "Las contraseñas no coinciden.")
        
       # Validación de seguridad de contraseña
        if password:
            if len(password) < 8:
                self.add_error('institution_password', 'La contraseña debe tener al menos 8 caracteres.')
            if not re.search(r'[A-Z]', password):
                self.add_error('institution_password', 'La contraseña debe contener al menos una mayúscula.')
            if not re.search(r'[0-9]', password):
                self.add_error('institution_password', 'La contraseña debe contener al menos un número.')
        
        return cleaned_data