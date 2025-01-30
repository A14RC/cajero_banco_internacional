from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, InicioSesionForm, TransferenciaForm, RetiroForm, PagoForm, ConsultaSaldoForm
from .models import Usuario, Transaccion
from django.contrib.auth.decorators import login_required

@login_required
def menu(request):
    nombre_usuario = request.user.nombre
    return render(request, 'menu.html', {'nombre_usuario': nombre_usuario})

def inicio(request):
    return render(request, 'inicio.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.saldo = form.cleaned_data.get('saldo')
            usuario.save()
            return redirect('inicio_sesion')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def inicio_sesion(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('menu')
            else:
                form.add_error(None, 'Correo o contraseña incorrectos')
    else:
        form = InicioSesionForm()
    return render(request, 'inicio_sesion.html', {'form': form})



@login_required
def transferencia(request):
    mensaje = None
    saldo = None
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            destinatario_email = form.cleaned_data.get('destinatario')
            monto = form.cleaned_data.get('monto')
            try:
                destinatario = Usuario.objects.get(email=destinatario_email)
                if request.user.saldo >= monto:
                    request.user.saldo -= monto
                    destinatario.saldo += monto
                    request.user.save()
                    destinatario.save()
                    Transaccion.objects.create(usuario=request.user, tipo='transferencia', monto=monto, descripcion='Transferencia realizada')
                    mensaje = 'Transferencia realizada con éxito'
                else:
                    mensaje = 'Saldo insuficiente'
            except Usuario.DoesNotExist:
                mensaje = 'El usuario no está registrado en nuestro banco'
            saldo = request.user.saldo
    else:
        form = TransferenciaForm()
    return render(request, 'transferencia.html', {'form': form, 'mensaje': mensaje, 'saldo': saldo})

@login_required
def retiro(request):
    mensaje = None
    saldo = None
    if request.method == 'POST':
        form = RetiroForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data.get('monto')
            if request.user.saldo >= monto:
                request.user.saldo -= monto
                request.user.save()
                Transaccion.objects.create(usuario=request.user, tipo='retiro', monto=monto, descripcion='Retiro realizado')
                mensaje = 'Retiro realizado con éxito'
            else:
                mensaje = 'Saldo insuficiente'
            saldo = request.user.saldo
    else:
        form = RetiroForm()
    return render(request, 'retiro.html', {'form': form, 'mensaje': mensaje, 'saldo': saldo})

@login_required
def pago(request):
    mensaje = None
    saldo = None
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data.get('monto')
            if request.user.saldo >= monto:
                request.user.saldo -= monto
                request.user.save()
                Transaccion.objects.create(usuario=request.user, tipo='pago', monto=monto, descripcion='Pago realizado')
                mensaje = 'Pago realizado con éxito'
            else:
                mensaje = 'Saldo insuficiente'
            saldo = request.user.saldo
    else:
        form = PagoForm()
    return render(request, 'pago.html', {'form': form, 'mensaje': mensaje, 'saldo': saldo})

@login_required
def consulta_saldo(request):
    saldo = None
    if request.method == 'POST':
        saldo = request.user.saldo
    return render(request, 'consulta_saldo.html', {'saldo': saldo})