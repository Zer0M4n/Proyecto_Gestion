from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.


# --- 1. Manager para tu Usuario Personalizado ---
# Necesitamos esto para decirle a Django cómo crear usuarios
# (ej. 'create_user' y 'create_superuser' para la consola)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        """
        Crea y guarda un Usuario con el email, teléfono y contraseña dados.
        """
        if not email:
            raise ValueError('El Email debe ser proporcionado')
        
        email = self.normalize_email(email)
        # Asignamos un status por defecto, '1' (ej. 'Activo')
        # Asume que ya creaste este status en tu tabla 'status' de Supabase
        extra_fields.setdefault('status_id', 1) 
        
        user = self.model(email=email, phone=phone, **extra_fields)
        
        # Django se encarga del HASHING automáticamente con set_password
        user.set_password(password) 
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        """
        Crea y guarda un superusuario.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status_id', 1) # Asume 1 = Activo

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone, password, **extra_fields)


# --- 2. Modelos de la Base de Datos ---
# Basados en tu esquema de Supabase

class Status(models.Model):
    # Tu esquema usa 'smallint' para ID, pero BigAutoField es el 
    # estándar de Django y es compatible.
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    class Meta:
        managed = False  # Django no debe crear ni borrar esta tabla
        db_table = 'public"."status' # Apunta a tu tabla existente
        verbose_name_plural = "Status"

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Omitimos 'id' para que Django use 'BigAutoField'
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255) # Django guardará el hash aquí
    creation_date = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20, unique=True)
    
    # Relación con Status
    status = models.ForeignKey(Status, on_delete=models.PROTECT, db_column='status')

    # Campos requeridos por Django Admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # Lo manejamos con 'status' pero es útil

    # Le decimos a Django que use 'email' para el login
    USERNAME_FIELD = 'email'
    
    # Campos requeridos al crear un usuario (ej. 'createsuperuser')
    REQUIRED_FIELDS = ['phone']

    # Asignamos el Manager
    objects = CustomUserManager()

    class Meta:
        managed = False # Django no debe crear ni borrar esta tabla
        db_table = 'public"."users' # Apunta a tu tabla existente

    def __str__(self):
        return self.email

# --- 3. Modelos de Perfiles ---

class Donee(models.Model):
    # Omitimos 'id'
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    first_surname = models.CharField(max_length=255)
    second_surname = models.CharField(max_length=255)
    curp = models.CharField(max_length=18, unique=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    
    # La relación clave con el Usuario
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed = False
        db_table = 'public"."donees'

    def __str__(self):
        return f"{self.first_name} {self.first_surname}"

class Donor(models.Model):
    # Omitimos 'id'
    created_at = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    first_surname = models.CharField(max_length=255)
    second_surname = models.CharField(max_length=255)
    curp = models.CharField(max_length=18, unique=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    
    # La relación clave con el Usuario
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed = False
        db_table = 'public"."donors'

    def __str__(self):
        return f"{self.first_name} {self.first_surname}"

class Institution(models.Model):
    # Omitimos 'id'
    created_at = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    # La relación clave con el Usuario
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, db_column='user')

    class Meta:
        managed = False
        db_table = 'public"."institutions'

    def __str__(self):
        return self.name