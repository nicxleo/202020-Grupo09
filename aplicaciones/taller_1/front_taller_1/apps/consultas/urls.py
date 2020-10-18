from django.urls import path

from apps.consultas import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('EjecutarRF1/<json>/', views.EjecutarRF1, name='EjecutarRF1'),
    path('EjecutarRF2/<json>/', views.EjecutarRF2, name='EjecutarRF2'),
    path('EjecutarRF3/<json>/', views.EjecutarRF3, name='EjecutarRF3'),
    path('EjecutarRA2/', views.EjecutarRA2, name='EjecutarRA2'),
    path('ConsultarRespuesta/<json>/', views.ConsultarRespuesta, name='ConsultarRespuesta')
]
