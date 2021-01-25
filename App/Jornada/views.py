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

def getallCandidatos():
    try:
        candidato = Candidato.objects.values()
        candidato_serializer = CandidatoSerializer(data=candidato)
        if candidato_serializer.is_valid:
            resultcandidato = [entry for entry in candidato]
            return resultcandidato
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
    splitdate = str(date.today()).split('-')
    year = splitdate[0][2]+splitdate[0][3]
    splitI = inicio.split('/')
    splitF = fin.split('/')
    monthI = splitI[1]
    if int(splitI[1])<10:
        monthI = splitI[1]
    dayI = splitI[0]
    if int(splitI[0])<10:
        dayI = splitI[0]
    monthF = splitF[1]
    if int(splitF[1])<10:
        monthF = splitF[1]
    dayF = splitF[0]
    if int(splitF[0])<10:
        dayF = splitF[0]
    return str(year+monthI+dayI+monthF+dayF+tipo)

def getJornada(request):
    if request.method == 'GET': #Retorna todas las jornadas con sus respectivos candidatos
        jornadas = getallJornada()
        candidatos = getallCandidatos()
        jornadacandidato = Jornada_candidato.objects.values()
        jornadacandidato_serializer = JornadaCandidatoSerializer(data=jornadacandidato)
        if jornadacandidato_serializer.is_valid and jornadas!=None and candidatos!=None: #Verifica que las entidades sean válidas
            requestjson = []
            resultjornadacandidato = [entry for entry in jornadacandidato]
            for i in range(len(jornadas)): #Obtiene la lista de candidatos asociados a cada jornada
                listcandidatos = []
                for j in range(len(resultjornadacandidato)):
                    if jornadas[i]['idJornada'] == resultjornadacandidato[j]['idJornada_id']:
                        try:
                            index = 0
                            for l in range(len(candidatos)):
                                if candidatos[l]['idCandidato'] == resultjornadacandidato[j]['idCandidato_id']:
                                    index = l
                                    break
                            record = {
                                'idCandidato':resultjornadacandidato[j]['idCandidato_id'],
                                'nombreCandidato':candidatos[index]['nombreCandidato'],
                                'foto':candidatos[index]['foto']
                            }
                            listcandidatos.append(record)
                        except:
                            jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                            return JsonResponse(jsonresponse,safe=False)

                record = {
                    'idJornada':jornadas[i]['idJornada'],
                    'nombreJornada':jornadas[i]['nombreJornada'],
                    'correoAdministrador':jornadas[i]['correoAdministrador_id'],
                    'fechaInicio':jornadas[i]['fechaInicio'],
                    'fechaFinal':jornadas[i]['fechaFinal'], 
                    "candidatos":listcandidatos,
                }
                requestjson.append(record)
            
            kindof = [] #Obtiene los tipos de jornadas que existen
            tipos = getallTipos() 
            for i in range(len(tipos)):
                kindof.append({"clave":tipos[i]['claveTipoJornada'],"descripcion":tipos[i]['descripcionTipoJornada']})
            
            return JsonResponse({"tipos":kindof,"jornadas":requestjson},safe=False)
        else: 
            jsonresponse = {"code":"NE-400","message":"Bad request"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'POST':#Crea una nueva jornada
        nueva_jornada = JSONParser().parse(request)
        idjornada = getidJornada(nueva_jornada['fechaInicio'],nueva_jornada['fechaFinal'],nueva_jornada['tipoJornada'])        
        njornada = {
            'idJornada':idjornada,
            'nombreJornada':nueva_jornada['nombreJornada'],
            'fechaInicio':nueva_jornada['fechaInicio'],
            'fechaFinal':nueva_jornada['fechaFinal'],
            'correoAdministrador':nueva_jornada['correoAdministrador'],
            'tipoJornada':nueva_jornada['tipoJornada']
        }
        jornada_serializer = JornadaSerializer(data=njornada)
        if jornada_serializer.is_valid(): #Valida los campos de la jornada
            try:
                jornada_serializer.save() #Guarda la jornada en la DB
                candidatos = [] #Arreglo para candidatos
                if len(nueva_jornada['candidatos'])>0: #La jornada incluye candidatos
                    for i in range(len(nueva_jornada['candidatos'])):
                        idcandidato = nueva_jornada['candidatos']
                        njornadacandidato = { #Elemento para la tabla jornada-candidato
                            'idJornadaCandidato':idjornada+str(idcandidato[i]),
                            'idJornada':idjornada,
                            'idCandidato':idcandidato[i],
                            'novotos':0
                        }
                        jornadacandidato_serializer = JornadaCandidatoSerializer(data=njornadacandidato)
                        if jornadacandidato_serializer.is_valid(): #Valida los campos de jornada-candidato
                            try:
                                jornadacandidato_serializer.save() #Guarda la tupla en jornada-candidato
                                auxcandidato = Candidato.objects.values().filter(idCandidato=idcandidato[i]) #Obtenemos el candidato registrado
                                print(auxcandidato)
                                if auxcandidato!=None: #Error al consultar al candidato registrado
                                    create = {
                                        'idCandidato': auxcandidato[0]['idCandidato'],
                                        'nombreCandidato': auxcandidato[0]['nombreCandidato'],
                                        'foto': str(auxcandidato[0]['foto'])
                                    }
                                    print(create)
                                    candidatos.append(create)
                                else:
                                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                                    return JsonResponse(jsonresponse,safe=False)
                            except:
                                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                                return JsonResponse(jsonresponse,safe=False)
                        else:
                            jsonresponse = {"code":"NE-400","message":"Bad request"}
                            return JsonResponse(jsonresponse,safe=False)

                auxjornada = Jornada.objects.values().filter(idJornada=idjornada) #Consulta de la jornada resultante
                cjornada = {
                    'idJornada':auxjornada[0]['idJornada'],
                    'nombreJornada':auxjornada[0]['nombreJornada'],
                    'fechaInicio':auxjornada[0]['fechaInicio'],
                    'fechaFinal':auxjornada[0]['fechaFinal'],
                    'correoAdministrador':auxjornada[0]['correoAdministrador_id'],
                    "candidatos": candidatos
                }
                return JsonResponse(cjornada,safe=False)
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)    
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