from django.contrib import admin
from .models import Jornada,Jornada_candidato,Jornada_votante

# Register your models here.
admin.site.register(Jornada)
admin.site.register(Jornada_candidato)
admin.site.register(Jornada_votante)