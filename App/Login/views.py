from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from App.Administrador.models import Administrador
from App.Administrador.serializers import AdministradorSerializer
from App.Votante.models import Votante
from App.Votante.serializers import VotanteSerializer
from App.Jornada.models import Jornada_votante,Jornada
from App.Jornada.serializers import JornadaSerializer,JornadaVotanteSerializer

# Create your views here.
def getLogin(request):
    if request.method == 'POST': #Login
        loginuser = JSONParser().parse(request)
        email = loginuser['correo']
        password = loginuser['password']
        if email.split('@')[1].split('.')[0] == 'administrador': #User = administrador
            usuario = Administrador.objects.values().filter(emailadmin=email)
            if usuario.exists(): #Verifica que el usuario existe
                if email==usuario[0]['emailadmin'] and password==usuario[0]['password']: #Credenciales correctas
                    response = {
                        'correoAdministrador':usuario[0]['emailadmin'],
                        'permisos': usuario[0]['permisos']
                    }
                    return JsonResponse(response,safe=False)
                else:
                    jsonresponse = {'code':'NE-400','message':'Bad request'}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {'code':'NE-404','message':'Not found'}
                return JsonResponse(jsonresponse,safe=False)
        else: #User = votante
            usuario = Votante.objects.values().filter(correoInstitucional=email)
            if usuario.exists(): #Verifica que el usuario existe
                if email==usuario[0]['correoInstitucional'] and password==usuario[0]['password']: #Credenciales correctas
                    votos = []
                    jornadas = Jornada.objects.values()
                    idvotante = usuario[0]['idVotante']
                    for i in range(len(jornadas)):
                        idjornada = jornadas[i]['idJornada']
                        jornadavotante = Jornada_votante.objects.values().filter(idJornada=idjornada,idVotante=idvotante)
                        if jornadavotante.exists():                      
                            votos.append({"idJornada":jornadas[i]['idJornada'],"nombreJornada":jornadas[i]['nombreJornada'],"voto":True})
                        else:
                            votos.append({"idJornada":jornadas[i]['idJornada'],"nombreJornada":jornadas[i]['nombreJornada'],"voto":False})
                    response = {
                        'idVotante':idvotante,
                        'nombreVotante':usuario[0]['nombreVotante'],
                        'votos':votos
                    }
                    return JsonResponse(response,safe=False)
                else:
                    jsonresponse = {'code':'NE-400','message':'Bad request'}
                    return JsonResponse(response,safe=False)
            else:
                jsonresponse = {'code':'NE-404','message':'Not found'}
                return JsonResponse(jsonresponse,safe=False) 
        jsonresponse = {'code':'NE-200','message':'Success'}
        return JsonResponse(jsonresponse,safe=False)