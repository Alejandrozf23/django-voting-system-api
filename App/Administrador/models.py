from django.db import models

# Create your models here.
class Administrador(models.Model):
    emailadmin = models.CharField(primary_key=True,null=False,blank=False,max_length=50)
    password = models.CharField(max_length=50,null=False)
    permisos = models.IntegerField()
    
    def __str__(self):
        return self.emailadmin