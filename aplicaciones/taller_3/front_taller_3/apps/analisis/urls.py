from django.urls import path

from apps.analisis import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('ResumenQuestions/<json>/', views.ResumenQuestions, name='ResumenQuestions'),
    path('ResumenAnswers/<json>/', views.ResumenAnswers, name='ResumenAnswers'),
    path('ResumenUsers/<json>/', views.ResumenUsers, name='ResumenUsers'),
    path('ResumenEntities/<json>/', views.ResumenEntities, name='ResumenEntities'),
    path('ResumenEntitiesQuestions/<json>/', views.ResumenEntitiesQuestions, name='ResumenEntitiesQuestions'),
    path('CountAnswer/<json>/', views.CountAnswer, name='CountAnswer'),
    path('CountLocation/<json>/', views.CountLocation, name='CountLocation'),
    path('CountScore/<json>/', views.CountScore, name='CountScore'),
    path('CountCurrency/<json>/', views.CountCurrency, name='CountCurrency'),
    path('CountSalaryDollar/<json>/', views.CountSalaryDollar, name='CountSalaryDollar'),
    path('CountSalaryEuro/<json>/', views.CountSalaryEuro, name='CountSalaryEuro'),
    path('CountSalaryPoundSterling/<json>/', views.CountSalaryPoundSterling, name='CountSalaryPoundSterling'),
    path('CountEmployees/<json>/', views.CountEmployees, name='CountEmployees'),
    path('CountTagQuestions/<json>/', views.CountTagQuestions, name='CountTagQuestions'),
    path('CountEntityQuestions/<json>/', views.CountEntityQuestions, name='CountEntityQuestions'),
    path('CountEntityAnswers/<json>/', views.CountEntityAnswers, name='CountEntityAnswers'),
    path('TablaCurrency/<json>/', views.TablaCurrency, name='TablaCurrency')
]
