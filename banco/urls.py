from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('inicio_sesion/', views.inicio_sesion, name='inicio_sesion'),
    path('menu/', views.menu, name='menu'),
    path('transferencia/', views.transferencia, name='transferencia'),
    path('retiro/', views.retiro, name='retiro'),
    path('pago/', views.pago, name='pago'),
    path('consulta_saldo/', views.consulta_saldo, name='consulta_saldo'),
]