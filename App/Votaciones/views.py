import json, requests
from Utils import jwt
from hashlib import sha256
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from App.Candidato.models import Candidato
from App.Candidato.serializers import CandidatoSerializer
from App.Votante.models import Votante,Tipo_Votante
from App.Votante.serializers import VotanteSerializer
from App.Jornada.models import Jornada_votante,Jornada,Jornada_candidato,Resultados
from App.Jornada.serializers import JornadaVotanteSerializer,JornadaCandidatoSerializer,JornadaSerializer,ResultadosSerializer

jwToken = jwt.JsonWebToken()

# Create your views here.
def getAllVotos(idcandidato,idjornada):
    novotos = 0
    result = Jornada_votante.objects.values().filter(idCandidato=idcandidato,idJornada=idjornada)
    for i in range(len(result)):
        novotos += 1
    return novotos

def getCandidatosByJornada(votosTotales):
    candidatosByJornada = []
    for i in range(len(votosTotales)):
        nombre = Candidato.objects.values().filter(idCandidato=votosTotales[i]['idCandidato_id'])[0]['nombreCandidato']
        candidatosByJornada.append({'idCandidato':votosTotales[i]['idCandidato_id'],'nombre':nombre})
    return candidatosByJornada

def getVotantesByJornada(votosParciales):
    votantesByJornada = []
    for i in range(len(votosParciales)):
        tipo = Votante.objects.values().filter(idVotante=votosParciales[i]['idVotante_id'])[0]['tipo_id']
        votantesByJornada.append({'idVotante':votosParciales[i]['idVotante_id'],'tipo':tipo})
    return votantesByJornada

def getCandidatosTotales(id,votosTotales,candidatosByJornada):
    totales = []
    for i in range(len(votosTotales)):
        novotos = getAllVotos(votosTotales[i]['idCandidato_id'],id)
        record = {
            'nombreCandidato':candidatosByJornada[i]['nombre'],
            'novotos':novotos
        }
        totales.append(record)
    return totales

def getCandidatosParciales(tipos_votantes,candidatosByJornada):
    parciales = []
    for i in range(len(tipos_votantes)):
        auxiliar = []
        for j in range(len(candidatosByJornada)):
            auxiliar.append({
                'nombreCandidato':candidatosByJornada[j]['nombre'],
                'novotos':0
            })
        record = {
            'tipo':tipos_votantes[i]['tipo'],
            'votos':auxiliar
        }
        parciales.append(record)
    return parciales

def getVotosParciales(votosParciales,votantesByJornada,candidatosByJornada,parciales):
    tiposDisponibles = Tipo_Votante.objects.values()
    for i in range(len(votosParciales)):
        idVotante = votosParciales[i]['idVotante_id']
        idCandidato = votosParciales[i]['idCandidato_id']
        for i in range(len(votantesByJornada)):
            if votantesByJornada[i]['idVotante'] == idVotante:
                tipoVotante = votantesByJornada[i]['tipo']
                for l in range(len(tiposDisponibles)):
                    if tiposDisponibles[l]['idtipovotante'] == tipoVotante:
                        indexTipo = l
                        break
                for l in range(len(candidatosByJornada)):
                    if candidatosByJornada[l]['idCandidato'] == idCandidato:
                        indexCandidato = l
                        break
                parciales[indexTipo]['votos'][indexCandidato]['novotos']+=1
                break
    return parciales

def validateEntidadesToVote(idCandidato,idVotante,idJornada):
    votante = Votante.objects.values().filter(idVotante=idVotante)
    candidato = Candidato.objects.values().filter(idCandidato=idCandidato)
    jornada_candidato = Jornada_candidato.objects.values().filter(idJornada=idJornada,idCandidato=idCandidato)
    jornada_votante = Jornada_votante.objects.values().filter(idJornada=idJornada,idVotante=idVotante)
    return True if votante.exists() and candidato.exists() and jornada_candidato.exists() and not jornada_votante.exists() else False

def buildJornadaVotante(idJornada,idVotante):
    jornadaVotante = {
        'idJornadaVotante':str(idJornada)+str(idVotante),
        'idVotante':idVotante,
        'idJornada':str(idJornada)
    }
    return jornadaVotante

def saveJornadaVotante(jornadaVotante_serializers):
    try:
        jornadaVotante_serializers.save()
        return True
    except:
        return False

def validateToken(jwtoken, votante):
    secret = jwToken.generateSecret(votante['access_code'],3)
    return jwToken.validateJWT(jwtoken, secret)

def validateRequest(tipoVotante, idVotante, idCandidato, access_code, firma):
    message = tipoVotante+idVotante+idCandidato+access_code
    hashSign = sha256(message.encode('utf-8')).hexdigest()
    if hashSign == firma:
        return True
    return False

def getVotaciones(request,id):
    if request.method == 'GET':
        votosTotales = Jornada_candidato.objects.values().filter(idJornada=id)
        votosParciales = Jornada_votante.objects.values().filter(idJornada=id).order_by('-idCandidato')

        votantesByJornada = getVotantesByJornada(votosParciales)
        candidatosByJornada = getCandidatosByJornada(votosTotales)

        tipos_votantes = Tipo_Votante.objects.values()
        totales = getCandidatosTotales(id,votosTotales,candidatosByJornada)
        parciales = getCandidatosParciales(tipos_votantes,candidatosByJornada)
        
        jsonresponse = {'totales':totales,'parciales':getVotosParciales(votosParciales,votantesByJornada,candidatosByJornada,parciales)}
        return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'POST':        
        data = JSONParser().parse(request)
        #datarequest = json.loads(data['data'])
        datarequest = data       
        headers = request.headers
        
        authorization = headers['Authorization']
        firma = headers['Firma']
        tipoVotante = datarequest['tipoVotante']
        idVotante = datarequest['idVotante']
        idCandidato = datarequest['idCandidato'] 
        
        votante = Votante.objects.values().filter(idVotante = idVotante)[0]
        responseToken = validateToken(authorization, votante)

        if not responseToken['code'] == 'NE-200':
            return JsonResponse(responseToken)
        
        if not validateRequest(tipoVotante, idVotante, idCandidato, votante['access_code'], firma):
            jsonresponse = {'code':'NE-401','message':'El mensaje ha sido modificado'}
            return JsonResponse(jsonresponse,safe=False)
        
        jornadaVotante_serializers = JornadaVotanteSerializer(data=buildJornadaVotante(id,idVotante))
        if jornadaVotante_serializers.is_valid(): 
            if saveJornadaVotante(jornadaVotante_serializers):
                jsonresponse = {'code':'NE-200','message':'Success'}
                return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {'code':'NE-500','message':'Lo siento. Algo salió mal'}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {'code':'NE-400','message':'Bad request'}
            return JsonResponse(jsonresponse,safe=False)