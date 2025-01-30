from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    saldo = forms.DecimalField(label='Saldo Inicial', max_digits=10, decimal_places=2)

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password1', 'password2', 'saldo']

class InicioSesionForm(forms.Form):
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class TransferenciaForm(forms.Form):
    destinatario = forms.EmailField(label='Correo del destinatario')
    monto = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2)

class RetiroForm(forms.Form):
    monto = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2)

class PagoForm(forms.Form):
    servicio = forms.CharField(label='Servicio')
    monto = forms.DecimalField(label='Monto', max_digits=10, decimal_places=2)

class ConsultaSaldoForm(forms.Form):
    pass  # No se necesita ningún campo para consultar el saldo