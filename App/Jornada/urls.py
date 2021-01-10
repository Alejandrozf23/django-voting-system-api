from django.urls import path
from .views import getJornada
from .views import editJornada

urlpatterns = [
    path('',getJornada,name='getJornada'),
    path('<str:id>/',editJornada,name='editJornada')
]