from django.db import models
from App.Administrador.models import Administrador

# Create your models here.
class Candidato(models.Model):
    idCandidato = models.CharField(primary_key=True,null=False,blank=False,max_length=11)
    nombreCandidato = models.CharField(max_length=50,null=False)
    propuestasGenerales = models.CharField(max_length=500)
    propuestaArchivo = models.TextField(null=False)
    foto = models.TextField(null=False)
    correoAdministrador = models.ForeignKey(Administrador,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombreCandidato