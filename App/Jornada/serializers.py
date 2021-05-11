from rest_framework import serializers 
from .models import Jornada,Jornada_candidato,Jornada_votante,Tipo_jornada,Resultados
 
class JornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada
        fields = ('idJornada','nombreJornada','fechaInicio','fechaFinal','correoAdministrador','tipoJornada','datos','jornada','candidatos','n','g')

class JornadaCandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada_candidato
        fields = ('idJornadaCandidato','idJornada','idCandidato')

class JornadaVotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jornada_votante
        fields = ('idJornadaVotante','idJornada','idVotante')

class ResultadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultados
        fields = ('noRastreo','idJornada','idCandidato','tipoVotante')

class TipoJornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_jornada
        fields = ('claveTipoJornada','descripcionTipoJornada')