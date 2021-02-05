import json,sys
from datetime import date,datetime
from django.shortcuts import render
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from random import randint,random
from .models import Candidato
from .serializers import CandidatoSerializer
from App.Jornada.models import Jornada,Jornada_candidato

def getidCandidato(nombre):
    dates = date.today()
    norandom = randint(0,100)
    splitname = nombre.split(' ')
    numbers = '0'+str(norandom) if norandom<10 else str(norandom)        
    name = splitname[0][0].upper()+splitname[len(splitname)-2][0].upper()+splitname[len(splitname)-1][0].upper() 
    year = str(dates.year)[2]+str(dates.year)[3]
    month = '0'+str(dates.month) if int(dates.month)<10 else str(dates.month)
    day = '0'+str(dates.day) if int(dates.day)<10 else str(dates.day)
    return numbers+name+year+month+day

def getDateFormat(actualDate):
    date = actualDate.split(' ')[0].split('/')
    time = actualDate.split(' ')[1].split(':')
    return datetime(int(date[2]),int(date[1]),int(date[0]),int(time[0]),int(time[1]),int(time[2]))

def getStatusCandidato(id):
    jornada_candidato = Jornada_candidato.objects.values().filter(idCandidato_id=id)
    if len(jornada_candidato)>0:
        idjornada = jornada_candidato[0]['idJornada_id']
        jornadas = Jornada.objects.values().filter(idJornada=idjornada)
        actual = datetime.now()
        fechaActual = datetime(actual.year,actual.month,actual.day,actual.hour,actual.minute,actual.second)
        for i in range(len(jornadas)): 
            fechaInicio = getDateFormat(jornadas[i]['fechaInicio'])
            fechaFinal = getDateFormat(jornadas[i]['fechaFinal'])
            if fechaActual>fechaInicio and fechaActual<fechaFinal:
                return True
    return False

def getCandidatoFromDB(candidato):
    record = {
        'idCandidato':candidato['idCandidato'],
        'nombreCandidato':candidato['nombreCandidato'],
        'propuestasGenerales':candidato['propuestasGenerales'],
        'propuestaArchivo':candidato['propuestaArchivo'],
        'foto':candidato['foto'],
        'correoAdministrador':candidato['correoAdministrador_id']
    }
    return record

def buildNewCandidato(idcandidato,candidato,email):
    dicts = {
        'idCandidato':idcandidato,
        'nombreCandidato':candidato['nombreCandidato'],
        'propuestasGenerales':candidato['propuestasGenerales'],
        'propuestaArchivo':candidato['propuestaArchivo'],
        'foto':candidato['foto'],
        'correoAdministrador':email
    }
    return dicts

def saveCandidatointoDB(candidato_serializer):
    try:
        candidato_serializer.save()
        return True
    except:
        return False

def deleteCandidatointoDB(candidato):
    try:
        candidato.delete()
        return True
    except:
        return False

# Create your views here.
def getCandidato(request):
    if request.method == 'GET':
        candidatos = Candidato.objects.values()
        candidato_serializer = CandidatoSerializer(data=candidatos)
        if candidato_serializer.is_valid:
            requestjson = []
            candidato = [entry for entry in candidatos]
            for i in range(len(candidato)): 
                requestjson.append(getCandidatoFromDB(candidato[i]))
            return JsonResponse(requestjson,safe=False)
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False) 
    
    if request.method == 'POST':
        candidato = JSONParser().parse(request)
        idcandidato = getidCandidato(candidato['nombreCandidato'])
        candidato_serializer = CandidatoSerializer(data=buildNewCandidato(idcandidato,candidato,candidato['correoAdministrador']))
        if candidato_serializer.is_valid():
            if saveCandidatointoDB(candidato_serializer):
                jsonresponse = {"code":"NE-0","message":"Success"}
                return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False)    
    
def editCandidato(request,id):
    if request.method == 'PUT':
        candidato = Candidato.objects.get(idCandidato=id)
        candidatoDB = Candidato.objects.values().filter(idCandidato=id)
        if candidatoDB.exists():
            if getStatusCandidato(str(id)):
                jsonresponse = {"code":"NE-409","message":"El candidato participa en una jornada activa"}
                return JsonResponse(jsonresponse,safe=False)
            candidatoUpdate = JSONParser().parse(request)
            candidato_serializer = CandidatoSerializer(candidato,data=buildNewCandidato(id,candidatoUpdate,candidatoDB[0]['correoAdministrador_id']))
            if candidato_serializer.is_valid():
                if saveCandidatointoDB(candidato_serializer):
                    jsonresponse = {"code":"NE-0","message":"Success"}
                    return JsonResponse(jsonresponse,safe=False)
                else:
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {"code":"NE-400","message":"Bad request"}
                return JsonResponse(jsonresponse,safe=False) 
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'DELETE':
        if Candidato.objects.values().filter(idCandidato=id).exists():
            candidato = Candidato.objects.get(idCandidato=id)
            if deleteCandidatointoDB(candidato):
                jsonresponse = {"idCandidato": id,"message":"Borrado con éxito"}
                return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)