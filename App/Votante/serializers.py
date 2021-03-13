from rest_framework import serializers 
from .models import Votante,Tipo_Votante
 
class TipoVotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Votante
        fields = ("idtipovotante","tipo")

class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = ('idVotante','nombreVotante','correoInstitucional','correoAdministrador','password','tipo','access_code')