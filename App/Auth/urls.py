from django.urls import path
from .views import authAccount

urlpatterns = [
    path('<str:id>/<str:token>/',authAccount,name='authAccount')
]