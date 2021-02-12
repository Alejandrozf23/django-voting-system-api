from django.urls import path
from .views import getLogin,restartPassword

urlpatterns = [
    path('',getLogin,name='getLogin'),
    path('restart-password/',restartPassword,name='restartPassword')
]