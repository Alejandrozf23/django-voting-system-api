from rest_framework import serializers 
from .models import Votos

class VotosSerializer(serializers.ModelSerializer):
   class Meta: 
      model = Votos
      fields = ('idVotos','idJornada','idCandidato','tipoVotante','noVotos')