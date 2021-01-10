import json,sys
from datetime import date
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Votante
from .models import Tipo_Votante
from .serializers import VotanteSerializer
from .serializers import TipoVotanteSerializer

def getallTipos():
    try:
        tipos = Tipo_Votante.objects.values()
        tipos_serializer = TipoVotanteSerializer(data=tipos)
        if tipos_serializer.is_valid:
            resulttipos = [entry for entry in tipos]
            return resulttipos
        else:
            return None
    except:
        return None

# Create your views here.
def getVotante(request):
    if request.method == 'GET': #Retorna todos los votantes
        votantes = Votante.objects.values() #Obtiene todos los votantes
        votante_serializer = VotanteSerializer(data=votantes)
        if votante_serializer.is_valid: #Valida los campos de votantes
            requestjson = []
            list_result = [entry for entry in votantes]
            for i in range(len(list_result)): 
                record = { #Obtiene cada votante
                    'idVotante':list_result[i]['idVotante'],
                    'nombreVotante':list_result[i]['nombreVotante'],
                    'correoInstitucional':list_result[i]['correoInstitucional'],
                    'correoAdministrador':list_result[i]['correoAdministrador_id']
                }
                requestjson.append(record)
            kindof = []
            tipos = getallTipos() 
            for i in range(len(tipos)):
                kindof.append({"clave":tipos[i]['idtipovotante'],"descripcion":tipos[i]['tipo']})
            return JsonResponse({"tipos":kindof,"votantes":requestjson},safe=False)
        else: 
            jsonresponse = [{"code":"NE-400","message":"Bad request"}]
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'POST': #Crea un nuevo votante
        response = []
        nuevo_votante = JSONParser().parse(request)
        for i in range(len(nuevo_votante)):
            dicts = { #Crea el nuevo elemento para Votante
                'idVotante':int(nuevo_votante[i]['idVotante']),
                'nombreVotante':nuevo_votante[i]['nombreVotante'],
                'correoInstitucional':nuevo_votante[i]['correoInstitucional'],
                'correoAdministrador':nuevo_votante[i]['correoAdministrador'],
                'password':nuevo_votante[i]['password'],
                'tipo':int(nuevo_votante[i]['tipo'])
            }
            votante_serializer = VotanteSerializer(data=dicts)
            if votante_serializer.is_valid(): #Valida los elementos del nuevo Votante
                try:
                    votante_serializer.save() #Guarda el Votante en la DB
                    registrados = {
                        'idVotante':int(nuevo_votante[i]['idVotante']),
                        'nombreVotante':nuevo_votante[i]['nombreVotante'],
                        'correoInstitucional':nuevo_votante[i]['correoInstitucional']
                    }
                    response.append(registrados)
                except:
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False) 
            else: 
                jsonresponse = {"code":"NE-400","message":"Bad request"}
                return JsonResponse(jsonresponse,safe=False) 
        return JsonResponse(response,safe=False)

def editVotante(request,id):
    if request.method == 'PUT':
        if Votante.objects.values().filter(idVotante=int(id)).exists(): #Verifica que el votante existe
            votante = Votante.objects.get(idVotante=int(id)) #Obtiene el votante
            edit_votante = JSONParser().parse(request)
            edit = { #Crea la actualización del votante
                'idVotante':int(id),
                'nombreVotante':edit_votante['nombreVotante'],
                'correoInstitucional':edit_votante['correoInstitucional'],
                'password':Votante.objects.values().filter(idVotante=int(id))[0]['password'],
                'correoAdministrador':Votante.objects.values().filter(idVotante=int(id))[0]['correoAdministrador_id'],
                'tipo':Votante.objects.values().filter(idVotante=int(id))[0]['tipo_id']
            }
            votante_serializer = VotanteSerializer(votante,data=edit)
            if votante_serializer.is_valid(): #Valida los campos de la actualización
                try:
                    votante_serializer.save() #Guarda la actualización en la DB
                    jsonresponse = {"code":"NE-200","message":"Success"}
                    return JsonResponse(jsonresponse,safe=False)
                except:
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {"code":"NE-400","message":"Bad request"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'DELETE':
        if Votante.objects.values().filter(idVotante=int(id)).exists(): #Verifica que el votante exista
            votante = Votante.objects.get(idVotante=int(id)) #Obtiene al votante
            try:
                votante.delete()#Elimina al votante
                jsonresponse = {"idVotante": id,"message":"Borrado con éxito"}
                return JsonResponse(jsonresponse,safe=False)
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)