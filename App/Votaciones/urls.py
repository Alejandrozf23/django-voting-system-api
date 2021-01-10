from django.urls import path
from .views import getVotaciones

urlpatterns = [
    path('<str:id>/',getVotaciones,name='getVotaciones')
]