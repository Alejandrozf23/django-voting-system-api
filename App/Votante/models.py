from django.db import models
from App.Administrador.models import Administrador

# Create your models here.
class Tipo_Votante(models.Model):
    idtipovotante = models.IntegerField(primary_key=True,null=False,blank=False)
    tipo = models.CharField(max_length=20,null=False)

class Votante(models.Model):
    idVotante = models.CharField(primary_key=True,null=False,blank=False,max_length=10)
    nombreVotante = models.CharField(max_length=50,null=False)
    correoInstitucional = models.CharField(max_length=40,null=False)
    password = models.CharField(max_length=64,null=False,blank=False)
    tipo = models.ForeignKey(Tipo_Votante,on_delete=models.CASCADE)
    correoAdministrador = models.ForeignKey(Administrador,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombreVotante