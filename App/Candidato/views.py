import json,sys
from datetime import date
from django.shortcuts import render
from django.core import serializers
from base64 import b64encode,b64decode
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from random import randint,uniform,random
from .models import Candidato
from .serializers import CandidatoSerializer

def getidCandidato(nombre):
    norand = randint(0,100)
    numbers = str(norand)
    if norand<10:
        numbers = '0'+str(norand)
    splitname = nombre.split(' ')
    name = splitname[0][0].upper()+splitname[len(splitname)-2][0].upper()+splitname[len(splitname)-1][0].upper() 
    splitdate = str(date.today()).split('-')
    year = splitdate[0][2]+splitdate[0][3]
    month = splitdate[1]
    day = splitdate[2]
    dates = year+month+day
    return numbers+name+dates

# Create your views here.
def getCandidato(request):
    if request.method == 'GET': #Retorna todos los candidatos
        candidatos = Candidato.objects.values() #Obtiene todos los candidatos
        candidato_serializer = CandidatoSerializer(data=candidatos)
        if candidato_serializer.is_valid: #Valida los campos de candidatos
            requestjson = []
            list_result = [entry for entry in candidatos]
            for i in range(len(list_result)): 
                record = { #Obtiene cada candidato
                    'idCandidato':list_result[i]['idCandidato'],
                    'nombreCandidato':list_result[i]['nombreCandidato'],
                    'propuestasGenerales':list_result[i]['propuestasGenerales'],
                    'propuestaArchivo':list_result[i]['propuestaArchivo'],
                    'foto':list_result[i]['foto'],
                    'correoAdministrador':list_result[i]['correoAdministrador_id']
                }
                requestjson.append(record)
            return JsonResponse(requestjson,safe=False)
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False) 
    
    if request.method == 'POST': #Crea un nuevo candidato
        nuevo_candidato = JSONParser().parse(request)
        idcandidato = getidCandidato(nuevo_candidato['nombreCandidato'])
        dicts = { #Crea el nuevo elemento para candidato
            'idCandidato':idcandidato,
            'nombreCandidato':nuevo_candidato['nombreCandidato'],
            'propuestasGenerales':nuevo_candidato['propuestasGenerales'],
            'propuestaArchivo':nuevo_candidato['propuestaArchivo'],
            'foto':nuevo_candidato['foto'],
            'correoAdministrador':nuevo_candidato['correoAdministrador']
        }
        candidato_serializer = CandidatoSerializer(data=dicts)
        if candidato_serializer.is_valid(): #Valida los elementos del nuevo candidato
            try:
                candidato_serializer.save() #Guarda el candidato en la DB
                registrocandidato = Candidato.objects.values().filter(idCandidato=idcandidato)
                jsonresponse = { #Crea el elemento para la respuesta
                    'idCandidato':registrocandidato[0]['idCandidato'],
                    'nombreCandidato':registrocandidato[0]['nombreCandidato'],
                    'propuestasGenerales':registrocandidato[0]['propuestasGenerales'],
                    'propuestaArchivo':registrocandidato[0]['propuestaArchivo'],
                    'foto':registrocandidato[0]['foto'],
                    'correoAdministrador':registrocandidato[0]['correoAdministrador_id']
                }
                return JsonResponse(jsonresponse,safe=False)
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)    
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False) 

def editCandidato(request,id):
    if request.method == 'PUT':
        if Candidato.objects.values().filter(idCandidato=id).exists(): #Verifica que el candidato existe
            candidato = Candidato.objects.get(idCandidato=id) #Obtiene el candidato
            edit_candidato = JSONParser().parse(request)
            edit = { #Crea la actualización del candidato
                'idCandidato':str(id),
                'nombreCandidato':edit_candidato['nombreCandidato'],
                'propuestasGenerales':edit_candidato['propuestasGenerales'],
                'propuestaArchivo':edit_candidato['propuestaArchivo'],
                'foto':edit_candidato['foto'],
                'correoAdministrador':Candidato.objects.values().filter(idCandidato=id)[0]['correoAdministrador_id']
            }
            candidato_serializer = CandidatoSerializer(candidato,data=edit)
            if candidato_serializer.is_valid(): #Valida los campos de la actualización
                try:
                    candidato_serializer.save() #Guarda la actualización en la DB
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
        if Candidato.objects.values().filter(idCandidato=id).exists(): #Verifica que el candidato exista
            candidato = Candidato.objects.get(idCandidato=id) #Obtiene al candidato
            try:
                candidato.delete()#Elimina al candidato
                jsonresponse = {"idCandidato": id,"message":"Borrado con éxito"}
                return JsonResponse(jsonresponse,safe=False)
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)