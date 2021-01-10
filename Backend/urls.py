from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jornadas/',include(('App.Jornada.urls','jornadas'))),
    path('jornadas/<str:id>/',include(('App.Jornada.urls','editjornadas'))),
    path('candidatos/',include(('App.Candidato.urls','candidatos'))),
    path('candidatos/<str:id>/',include(('App.Candidato.urls','editcandidatos'))),
    path('votantes/',include(('App.Votante.urls','votantes'))),
    path('votantes/<str:id>/',include(('App.Votante.urls','editvotantes'))),
    path('login/',include(('App.Login.urls','login'))),
    path('votaciones/',include(('App.Votaciones.urls','votaciones'))),
]
