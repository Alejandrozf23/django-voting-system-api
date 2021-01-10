from rest_framework import serializers 
from .models import Candidato

class CandidatoSerializer(serializers.ModelSerializer):
   class Meta: 
      model = Candidato
      fields = ('idCandidato','nombreCandidato','propuestasGenerales','propuestaArchivo','foto','correoAdministrador')
