from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(email=self.normalize_email(email), nombre=nombre)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email, nombre, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email

class Transaccion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
