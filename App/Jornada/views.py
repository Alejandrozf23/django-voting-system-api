import json,sys
from datetime import date
from django.shortcuts import render
from django.core import serializers
from rest_framework.parsers import JSONParser
from base64 import b64encode,b64decode
from django.http import JsonResponse
from .models import Jornada,Jornada_candidato,Tipo_jornada
from .serializers import JornadaSerializer
from .serializers import TipoJornadaSerializer
from .serializers import JornadaCandidatoSerializer
from App.Candidato.models import Candidato
from App.Candidato.serializers import CandidatoSerializer

# Create your views here.
def getallJornada():
    try:
        jornada = Jornada.objects.values()
        jornada_serializer = JornadaSerializer(data=jornada)
        if jornada_serializer.is_valid:
            resultjornada = [entry for entry in jornada]
            return resultjornada
        else:
            return None
    except:
        return None

def getallTipos():
    try:
        tipos = Tipo_jornada.objects.values()
        tipos_serializer = TipoJornadaSerializer(data=tipos)
        if tipos_serializer.is_valid:
            resulttipos = [entry for entry in tipos]
            return resulttipos
        else:
            return None
    except:
        return None

def getidJornada(inicio,fin,tipo):
    splitdate = str(date.today().year)
    year = splitdate[2]+splitdate[3]
    splitI = inicio.split('/')
    splitF = fin.split('/')
    monthI = splitI[1]
    dayI = splitI[0]
    monthF = splitF[1]    
    dayF = splitF[0]
    return str(year+monthI+dayI+monthF+dayF+tipo)

def getCandidatosByJornada(idjornada):
    listcandidatos = []
    candidatos = Jornada_candidato.objects.values().filter(idJornada=idjornada)
    for i in range(len(candidatos)):
        idcandidato = candidatos[i]['idCandidato_id']
        consultaCandidato = Candidato.objects.values().filter(idCandidato=idcandidato)
        listcandidatos.append(consultaCandidato[0])
    return listcandidatos

def getJornadaWithCandididatos(idjornada):
    listcandidatos = getCandidatosByJornada(idjornada)
    jornada = Jornada.objects.values().filter(idJornada=idjornada)
    record = {
        'idJornada':jornada[0]['idJornada'],
        'nombreJornada':jornada[0]['nombreJornada'],
        'correoAdministrador':jornada[0]['correoAdministrador_id'],
        'fechaInicio':jornada[0]['fechaInicio'],
        'fechaFinal':jornada[0]['fechaFinal'], 
        "candidatos":listcandidatos,
    }
    return record

def getTypesOfCandidatos():
    kindof = []
    tipos = getallTipos() 
    for i in range(len(tipos)):
        kindof.append({"clave":tipos[i]['claveTipoJornada'],"descripcion":tipos[i]['descripcionTipoJornada']})
    return kindof

def buildNewJornada(idjornada,nueva_jornada):        
    njornada = {
        'idJornada':idjornada,
        'nombreJornada':nueva_jornada['nombreJornada'],
        'fechaInicio':nueva_jornada['fechaInicio'],
        'fechaFinal':nueva_jornada['fechaFinal'],
        'correoAdministrador':nueva_jornada['correoAdministrador'],
        'tipoJornada':nueva_jornada['tipoJornada']
    }
    return njornada

def buildNewJornadaCandidato(idjornada,idcandidato):
    jornadacandidato = {
        'idJornadaCandidato':idjornada+str(idcandidato),
        'idJornada':idjornada,
        'idCandidato':idcandidato
    }
    return jornadacandidato

def assignCandidatosToJornada(idjornada,candidatos):
    registrados = []
    if len(candidatos)>0:
        for i in range(len(candidatos)):
            jcserializer = JornadaCandidatoSerializer(data=buildNewJornadaCandidato(idjornada,candidatos[i]))
            if jcserializer.is_valid():
                try:
                    jcserializer.save()
                    registrados.append(candidatos[i])
                except:
                    manageExceptionsFromCandidatos(registrados)
                    return False
    return True    

def manageExceptionsFromCandidatos(registrados):
    for i in range(len(registrados)):
        jornadacandidato = Jornada_candidato.objects.get(idCandidato=registrados[i])
        jornadacandidato.delete()

def getJornada(request):
    if request.method == 'GET': #Retorna todas las jornadas con sus respectivos candidatos
        jornadas = getallJornada()
        if jornadas!=None:
            requestjson = []
            kindof = getTypesOfCandidatos()
            for i in range(len(jornadas)):
                requestjson.append(getJornadaWithCandididatos(jornadas[i]['idJornada']))
            return JsonResponse({"tipos":kindof,"jornadas":requestjson},safe=False)
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'POST':
        nueva_jornada = JSONParser().parse(request)
        idjornada = getidJornada(nueva_jornada['fechaInicio'],nueva_jornada['fechaFinal'],nueva_jornada['tipoJornada'])
        jornada_serializer = JornadaSerializer(data=buildNewJornada(idjornada,nueva_jornada))
        if jornada_serializer.is_valid():
            try:
                jornada_serializer.save()
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
            if not assignCandidatosToJornada(idjornada,nueva_jornada['candidatos']):
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
            jornada = getJornadaWithCandididatos(idjornada)
            return JsonResponse(jornada,safe=False)   
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False)

def editJornada(request,id):
    if request.method == 'GET':
        if Jornada.objects.values().filter(idJornada=id).exists(): #Valida que la jornada existe
            jornada = Jornada.objects.values().filter(idJornada=id)[0] #Obtiene la jornada
            candidatos = getallCandidatos()
            jornadacandidato = Jornada_candidato.objects.values()
            jornadacandidato_serializer = JornadaCandidatoSerializer(data=jornadacandidato)
            if jornadacandidato_serializer.is_valid and candidatos!=None: #Verifica que las entidades sean válidas
                resultjornadacandidato = [entry for entry in jornadacandidato]
                listcandidatos = []
                for j in range(len(resultjornadacandidato)):
                    if id == resultjornadacandidato[j]['idJornada_id']:
                        try:
                            index = 0
                            for l in range(len(candidatos)):
                                if candidatos[l]['idCandidato'] == resultjornadacandidato[j]['idCandidato_id']:
                                    index = l
                                    break
                            record = {
                                'idCandidato':resultjornadacandidato[j]['idCandidato_id'],
                                'nombreCandidato':candidatos[index]['nombreCandidato'],
                                'propuestasGenerales':candidatos[index]['propuestasGenerales'],
                                'propuestaArchivo':candidatos[index]['propuestaArchivo'],
                                'foto':candidatos[index]['foto'],
                                'correoAdministrador':candidatos[index]['correoAdministrador_id']
                            }
                            listcandidatos.append(record)
                        except:
                            jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                            return JsonResponse(jsonresponse,safe=False)
                record = {
                    'idJornada':jornada['idJornada'],
                    'nombreJornada':jornada['nombreJornada'],
                    'correoAdministrador':jornada['correoAdministrador_id'],
                    'fechaInicio':jornada['fechaInicio'],
                    'fechaFinal':jornada['fechaFinal'], 
                    "candidatos":listcandidatos,
                }
                return JsonResponse(record,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)

    if request.method == 'PUT':
        if Jornada.objects.values().filter(idJornada=id).exists(): #Valida que la jornada existe
            edit_jornada = JSONParser().parse(request)
            for i in range(len(edit_jornada)):
                njornadacandidato = { #Elemento para la tabla jornada-candidato
                    'idJornadaCandidato':str(id)+str(edit_jornada[i]),
                    'idJornada':id,
                    'idCandidato':edit_jornada[i],
                    'novotos':0
                }
                jornadacandidato_serializer = JornadaCandidatoSerializer(data=njornadacandidato)
                if jornadacandidato_serializer.is_valid(): #Valida los campos de jornada-candidato
                    try:
                        jornadacandidato_serializer.save() #Guarda la tupla en jornada-candidato
                    except:
                        jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                        return JsonResponse(jsonresponse,safe=False)
            jsonresponse = {"code":"NE-200","message":"Success"}
            return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'DELETE':
        if Jornada.objects.values().filter(idJornada=id).exists(): #Valida que la jornada existe
            jornada = Jornada.objects.get(idJornada=id) #Obtiene la jornada
            jornada.delete() #Elimina la jornada
            jsonresponse = {"idJornada": id,"message":"Borrado con éxito"}
            return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)