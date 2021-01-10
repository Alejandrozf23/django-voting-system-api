from django.urls import path
from .views import getLogin

urlpatterns = [
    path('',getLogin,name='getLogin')
]