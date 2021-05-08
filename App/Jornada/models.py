from django.db import models
from App.Administrador.models import Administrador
from App.Candidato.models import Candidato
from App.Votante.models import Votante, Tipo_Votante

# Create your models here.
class Tipo_jornada(models.Model):
    claveTipoJornada = models.CharField(primary_key=True,null=False,blank=False,max_length=1)
    descripcionTipoJornada = models.CharField(max_length=50,null=False)

class Jornada(models.Model):
    idJornada = models.CharField(primary_key=True,null=False,blank=False,max_length=11)
    nombreJornada = models.CharField(max_length=150,null=False)
    fechaInicio = models.CharField(max_length=150,null=False,default="00/00/0000 00:00:00")
    fechaFinal = models.CharField(max_length=150,null=False,default="00/00/0000 00:00:00")
    correoAdministrador = models.ForeignKey(Administrador,on_delete=models.CASCADE)
    tipoJornada = models.ForeignKey(Tipo_jornada,on_delete=models.CASCADE)
    datos = models.CharField(max_length=64,null=True,blank=False)
    jornada = models.CharField(max_length=64,null=True,blank=False)
    candidatos = models.CharField(max_length=64,null=True,blank=False)
    n = models.TextField(null=True)
    g = models.TextField(null=True)

    class Meta:
        verbose_name = "Jornada"
        verbose_name_plural = "Jornadas"
    
    def __str__(self):
        return self.nombreJornada

class Jornada_candidato(models.Model):
    idJornadaCandidato = models.CharField(primary_key=True,null=False,blank=False,max_length=22)
    idJornada = models.ForeignKey(Jornada,on_delete=models.CASCADE,db_column='idJornada')
    idCandidato = models.ForeignKey(Candidato,on_delete=models.CASCADE,db_column='idCandidato')
    
    class Meta:
        unique_together = (('idJornada','idCandidato'),)

class Jornada_votante(models.Model):
    idJornadaVotante = models.CharField(primary_key=True,null=False,blank=False,max_length=22)
    idJornada = models.ForeignKey(Jornada,on_delete=models.CASCADE,db_column='idJornada')
    idVotante = models.ForeignKey(Votante,on_delete=models.CASCADE,db_column='idVotante')
    class Meta:
        unique_together = (('idJornada','idVotante'),)

class Resultados(models.Model):
    idResultados = models.AutoField(primary_key=True,null=False,blank=False)
    idJornada = models.ForeignKey(Jornada,on_delete=models.CASCADE,db_column='idJornada')
    idCandidato  = models.ForeignKey(Candidato,on_delete=models.CASCADE,db_column='idCandidato')
    tipoVotante = models.ForeignKey(Tipo_Votante,on_delete=models.CASCADE,db_column='tipoVotante')
    noRastreo = models.CharField(max_length=64,null=False,blank=False,db_column='noRastreo')