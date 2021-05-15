from django.urls import path
from .views import getVotaciones, getResultados

urlpatterns = [
    path('<str:id>/',getVotaciones,name='getVotaciones'),
    path('resultados/<str:id>/',getResultados,name='getResultados')
]