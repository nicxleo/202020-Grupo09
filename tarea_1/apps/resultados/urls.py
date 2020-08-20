from django.urls import path

from apps.resultados import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('EjecutarReto/<json>/', views.EjecutarReto, name='EjecutarReto'),
]
