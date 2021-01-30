import json,sys
from datetime import date,datetime
from django.shortcuts import render
from django.core import serializers
from base64 import b64encode,b64decode
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from random import randint,uniform,random
from .models import Candidato
from .serializers import CandidatoSerializer
from App.Jornada.models import Jornada,Jornada_candidato

def getidCandidato(nombre):
    norandom = randint(0,100)
    numbers = str(norandom)
    if norandom<10:
        numbers = '0'+str(norandom)
    splitname = nombre.split(' ')
    name = splitname[0][0].upper()+splitname[len(splitname)-2][0].upper()+splitname[len(splitname)-1][0].upper() 
    dates = date.today()
    year = str(dates.year)[2]+str(dates.year)[3]
    month = '0'+str(dates.month) if int(dates.month)<10 else str(dates.month)
    day = '0'+str(dates.day) if int(dates.day)<10 else str(dates.day)
    return numbers+name+year+month+day

def getStatusCandidato(id):
    jornada_candidato = Jornada_candidato.objects.values().filter(idCandidato_id=id)
    if len(jornada_candidato)>0:
        idjornada = jornada_candidato[0]['idJornada_id']
        jornadas = Jornada.objects.values().filter(idJornada=idjornada)
        actual = datetime.now()
        fechaActual = datetime(actual.year,actual.month,actual.day,actual.hour,actual.minute,actual.second)
        for i in range(len(jornadas)):            
            dateInit = jornadas[i]['fechaInicio'].split(' ')
            dateFinal = jornadas[i]['fechaFinal'].split(' ')
            dateSplit = dateInit[0].split('/')
            timeSplit = dateInit[1].split(':')
                        
            fechaInicio = datetime(int(dateSplit[2]),int(dateSplit[1]),int(dateSplit[0]),int(timeSplit[0]),int(timeSplit[1]),int(timeSplit[2]))

            dateSplit = dateFinal[0].split('/')
            timeSplit = dateFinal[1].split(':')

            fechaFinal = datetime(int(dateSplit[2]),int(dateSplit[1]),int(dateSplit[0]),int(timeSplit[0]),int(timeSplit[1]),int(timeSplit[2]))

            if fechaActual>fechaInicio and fechaActual<fechaFinal: #Candidato participa en Jornada activa
                return True
        return False
    else:
        return False

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
        candidato = Candidato.objects.get(idCandidato=id) #Obtiene el candidato
        if Candidato.objects.values().filter(idCandidato=id).exists(): #Verifica que el candidato existe
            if getStatusCandidato(str(id)):
                jsonresponse = {"code":"NE-409","message":"El candidato participa en una jornada activa"}
                return JsonResponse(jsonresponse,safe=False)
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
                candidato.delete() #Elimina al candidato
                jsonresponse = {"idCandidato": id,"message":"Borrado con éxito"}
                return JsonResponse(jsonresponse,safe=False)
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)