from django.urls import path
from .views import getVotante,editVotante

urlpatterns = [
    path('',getVotante,name='getVotante'),
    path('<str:id>/',editVotante,name='editVotante')
]