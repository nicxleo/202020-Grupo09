from django.urls import path

from apps.analisis import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('CountLocation/<json>/', views.CountLocation, name='CountLocation')
]
