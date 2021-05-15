from django.db import models
from App.Jornada.models import Jornada
from App.Votante.models import Tipo_Votante
from App.Candidato.models import Candidato

# Create your models here.
class Votos(models.Model):
    idVotos = models.AutoField(primary_key=True)
    idJornada = models.ForeignKey(Jornada, on_delete=models.CASCADE, db_column='idJornada')
    idCandidato  = models.TextField(null=False, blank=False, db_column='idCandidato')
    tipoVotante = models.ForeignKey(Tipo_Votante, on_delete=models.CASCADE, db_column='tipoVotante')
    noVotos = models.IntegerField(null=False, blank=False, db_column='noVotos')