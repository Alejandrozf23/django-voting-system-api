from django.urls import path
from .views import getCandidato
from .views import editCandidato

urlpatterns = [
    path('',getCandidato,name='getCandidato'),
    path('<str:id>/',editCandidato,name='editCandidato')
]