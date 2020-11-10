from django.urls import path

from apps.analisis import views

urlpatterns = [
    path('', views.Inicio, name='Inicio'),
    path('TablaTag/<json>/', views.TablaTag, name='TablaTag'),
    path('CountScale/<json>/', views.CountScale, name='CountScale'),
    path('CountTag/<json>/', views.CountTag, name='CountTag'),
    path('CountSubjectivity/<json>/', views.CountSubjectivity, name='CountSubjectivity'),
    path('CountDate/<json>/', views.CountDate, name='CountDate'),
    path('CountRetweeted/<json>/', views.CountRetweeted, name='CountRetweeted'),
    path('ResumenTweet/<json>/', views.ResumenTweet, name='ResumenTweet'),
    path('ResumenWord/<json>/', views.ResumenWord, name='ResumenWord'),
]
