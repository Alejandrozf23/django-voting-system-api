from rest_framework import serializers 
from .models import Jornada,Jornada_candidato,Jornada_votante,Tipo_jornada
 
class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = ('idJornada','nombreJornada','fechaInicio','fechaFinal','correoAdministrador','tipoJornada')

class JornadaCandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada_candidato
        fields = ('idJornadaCandidato','idJornada','idCandidato','novotos')

class JornadaVotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada_votante
        fields = ('idJornadaVotante','idJornada','idVotante','idCandidato')

class TipoJornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_jornada
        fields = ('claveTipoJornada','descripcionTipoJornada')