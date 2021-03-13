from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jornadas/',include(('App.Jornada.urls','jornadas'))),
    path('candidatos/',include(('App.Candidato.urls','candidatos'))),
    path('votantes/',include(('App.Votante.urls','votantes'))),
    path('login/',include(('App.Login.urls','login'))),
    path('votaciones/',include(('App.Votaciones.urls','votaciones'))),
]
