from django.urls import path
from .views import getLogin,restartPassword,accessCode

urlpatterns = [
    path('',getLogin,name='getLogin'),
    path('restart-password/',restartPassword,name='restartPassword'),
    path('access-code/',accessCode,name='accessCode')
]