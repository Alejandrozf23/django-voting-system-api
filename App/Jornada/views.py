from datetime import date
from django.core import serializers
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from . import models
from . import serializers
from App.Candidato.models import Candidato
from App.Votaciones.models import Votos

# Create your views here.
def getallJornada():
    try:
        jornada = models.Jornada.objects.values()
        jornada_serializer = serializers.JornadaSerializer(data=jornada)
        if jornada_serializer.is_valid:
            resultjornada = [entry for entry in jornada]
            return resultjornada
        else:
            return None
    except:
        return None

def getallTipos():
    try:
        tipos = models.Tipo_jornada.objects.values()
        tipos_serializer = serializers.TipoJornadaSerializer(data=tipos)
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
    candidatos = models.Jornada_candidato.objects.values().filter(idJornada=idjornada)
    for i in range(len(candidatos)):
        idcandidato = candidatos[i]['idCandidato_id']
        consultaCandidato = Candidato.objects.values().filter(idCandidato=idcandidato)
        listcandidatos.append(consultaCandidato[0])
    return listcandidatos

def getJornadaWithCandididatos(idjornada):
    listcandidatos = getCandidatosByJornada(idjornada)
    jornada = models.Jornada.objects.values().filter(idJornada=idjornada)
    publicKey = {'n':jornada[0]['n'],'g':jornada[0]['g']}
    votos = len(Votos.objects.values().filter(idJornada=idjornada))>0
    record = {
        'idJornada':jornada[0]['idJornada'],
        'nombreJornada':jornada[0]['nombreJornada'],
        'correoAdministrador':jornada[0]['correoAdministrador_id'],
        'fechaInicio':jornada[0]['fechaInicio'],
        'fechaFinal':jornada[0]['fechaFinal'],
        'publicKey':publicKey,
        'candidatos':listcandidatos,
        'descifrado':votos
    }
    return record

def getTypesOfCandidatos():
    kindof = []
    tipos = getallTipos() 
    for i in range(len(tipos)):
        kindof.append({"clave":tipos[i]['claveTipoJornada'],"descripcion":tipos[i]['descripcionTipoJornada']})
    return kindof

def buildNewJornada(idjornada,nueva_jornada):    
    publicKey = nueva_jornada['publicKey']
    njornada = {
        'idJornada':idjornada,
        'nombreJornada':nueva_jornada['nombreJornada'],
        'fechaInicio':nueva_jornada['fechaInicio'],
        'fechaFinal':nueva_jornada['fechaFinal'],
        'correoAdministrador':nueva_jornada['correoAdministrador'],
        'tipoJornada':nueva_jornada['tipoJornada'],
        'datos':None,
        'jornada':None,
        'candidatos':None,
        'n':publicKey['n'],
        'g':publicKey['g']
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
            if addCandidatoToJornada(idjornada,candidatos[i]):
                registrados.append(candidatos[i])
            else:
                manageExceptionsFromCandidatos(idjornada,registrados)
                return False
    return True    

def manageExceptionsFromCandidatos(idjornada,registrados):
    for i in range(len(registrados)):
        jornadacandidato = models.Jornada_candidato.objects.get(idJornada=idjornada,idCandidato=registrados[i])
        jornadacandidato.delete()

def addCandidatoToJornada(idjornada,idcandidato): 
    jcserializer = serializers.JornadaCandidatoSerializer(data=buildNewJornadaCandidato(idjornada,idcandidato))
    if jcserializer.is_valid():
        try:
            jcserializer.save()
            return True
        except:
            return False
    return False

def deleteCandidatoFromJornada(idjornada,idcandidato):    
    if models.Jornada_candidato.objects.values().filter(idJornada=idjornada,idCandidato=idcandidato).exists():
        jornadacandidato = models.Jornada_candidato.objects.get(idJornada=idjornada,idCandidato=idcandidato)
        try:
            jornadacandidato.delete()
            return True
        except:
            return False
    return False

def isCandidatoOnTheList(lista,idcandidato):
    if idcandidato in lista:
        return True
    return False

def editCandidatosFromJornadaCandidato(idjornada,candidatosRequest,candidatosDatabase):
    agregados = []
    eliminados = []
    if len(candidatosRequest)>0:
        for i in range(len(candidatosRequest)):
            if not isCandidatoOnTheList(candidatosDatabase,candidatosRequest[i]):
                if addCandidatoToJornada(idjornada,candidatosRequest[i]):
                    agregados.append(candidatosRequest[i])
                else:
                    manageExceptionsFromCandidatos(idjornada,agregados)
                    manageExceptionsFromCandidatos(idjornada,eliminados)
                    return False
        for i in range(len(candidatosDatabase)):
            if not isCandidatoOnTheList(candidatosRequest,candidatosDatabase[i]):
                if deleteCandidatoFromJornada(idjornada,candidatosDatabase[i]):
                    eliminados.append(candidatosDatabase[i])
                else:
                    manageExceptionsFromCandidatos(idjornada,agregados)
                    manageExceptionsFromCandidatos(idjornada,eliminados)
                    return False
    return True

def getJornada(request):
    if request.method == 'GET':
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
        jornada_serializer = serializers.JornadaSerializer(data=buildNewJornada(idjornada,nueva_jornada))
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
        if models.Jornada.objects.values().filter(idJornada=id).exists(): 
            jornada = models.Jornada.objects.values().filter(idJornada=id)[0]
            record = getJornadaWithCandididatos(jornada['idJornada'])            
            return JsonResponse(record,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)

    if request.method == 'PUT':
        if models.Jornada.objects.values().filter(idJornada=id).exists():
            candidatosRequest = JSONParser().parse(request)
            candidatos = models.Jornada_candidato.objects.values().filter(idJornada=id)            
            if len(candidatos)>0:
                candidatosDatabase = []
                database = [entry for entry in candidatos]
                for i in range(len(database)):
                    candidatosDatabase.append(database[i]['idCandidato_id'])
                if not editCandidatosFromJornadaCandidato(id,candidatosRequest,candidatosDatabase):
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                if not assignCandidatosToJornada(id,candidatosRequest):
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False)
            jsonresponse = {"code":"NE-200","message":"Success"}
            return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'DELETE':
        if models.Jornada.objects.values().filter(idJornada=id).exists():
            jornada = models.Jornada.objects.get(idJornada=id)
            try:
                jornada.delete()
            except:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)    
            jsonresponse = {"idJornada": id,"message":"Borrado con éxito"}
            return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)