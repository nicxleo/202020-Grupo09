from django.urls import path

from apps.consultas import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('EjecutarRF1/<json>/', views.EjecutarRF1, name='EjecutarRF1'),
    path('EjecutarRF2/<json>/', views.EjecutarRF2, name='EjecutarRF2'),
]
