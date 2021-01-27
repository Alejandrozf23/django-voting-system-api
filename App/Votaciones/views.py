from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from App.Candidato.models import Candidato
from App.Candidato.serializers import CandidatoSerializer
from App.Votante.models import Votante,Tipo_Votante
from App.Votante.serializers import VotanteSerializer
from App.Jornada.models import Jornada_votante,Jornada,Jornada_candidato
from App.Jornada.serializers import JornadaVotanteSerializer,JornadaCandidatoSerializer,JornadaSerializer

# Create your views here.
def getAllVotos(idcandidato,idjornada):
    novotos = 0
    result = Jornada_votante.objects.values().filter(idCandidato=idcandidato,idJornada=idjornada)
    if len(result)>0:
        for i in range(len(result)):
            novotos += 1
        return novotos
    else:
        return 0


def getVotaciones(request,id):
    if request.method == 'GET':
        total = []
        parcial = []
        votosT = Jornada_candidato.objects.values().filter(idJornada=id)
        votosP = Jornada_votante.objects.values().filter(idJornada=id).order_by('-idCandidato')
        
        votantesporjornada = []
        candidatosporjornada = []
        for i in range(len(votosT)):
            nombre = Candidato.objects.values().filter(idCandidato=votosT[i]['idCandidato_id'])[0]['nombreCandidato']
            candidatosporjornada.append({'idCandidato':votosT[i]['idCandidato_id'],'nombre':nombre})
        for i in range(len(votosP)):
            tipo = Votante.objects.values().filter(idVotante=votosP[i]['idVotante_id'])[0]['tipo_id']
            votantesporjornada.append({'idVotante':votosP[i]['idVotante_id'],'tipo':tipo})

        for i in range(len(votosT)): #Ciclo para votos totales
            novotos = getAllVotos(votosT[i]['idCandidato_id'],id)
            for j in range(len(candidatosporjornada)):
                record = {
                    'nombreCandidato':candidatosporjornada[i]['nombre'],
                    'novotos':novotos
                }
            total.append(record)
        
        tipos_votantes = Tipo_Votante.objects.values()
        for i in range(len(tipos_votantes)):
            auxiliar = []
            for j in range(len(candidatosporjornada)):
                auxiliar.append({
                    'nombreCandidato':candidatosporjornada[j]['nombre'],
                    'novotos':0
                })
            record = {
                'tipo':tipos_votantes[i]['tipo'],
                'votos':auxiliar
            }
            parcial.append(record)

        tiposdisponibles = Tipo_Votante.objects.values()
        for i in range(len(votosP)):
            idvotante = votosP[i]['idVotante_id']
            idcandidato = votosP[i]['idCandidato_id']
            for j in range(len(votantesporjornada)):
                if votantesporjornada[i]['idVotante'] == idvotante:
                    tipovotante = votantesporjornada[i]['tipo'] 
                    for l in range(len(tiposdisponibles)):
                        if tiposdisponibles[l]['idtipovotante'] == tipovotante:
                            indextipo = l
                            break
                    for l in range(len(candidatosporjornada)):
                        if candidatosporjornada[l]['idCandidato'] == idcandidato:
                            indexcandidato = l
                            break
                    parcial[indextipo]['votos'][indexcandidato]['novotos']+=1
                    break
        jsonresponse = {'totales':total,'parciales':parcial}
        return JsonResponse(jsonresponse,safe=False)
    
    if request.method == 'POST':
        #Obtiene los ID de los objetos
        datarequest = JSONParser().parse(request)
        idvotante = datarequest['idVotante']
        idcandidato = datarequest['idCandidato']
        #Obtiene los objetos de la DB
        candidato = Candidato.objects.values().filter(idCandidato=idcandidato)
        jornadac = Jornada_candidato.objects.values().filter(idJornada=id,idCandidato=idcandidato)
        votante = Votante.objects.values().filter(idVotante=idvotante)
        jornadav = Jornada_votante.objects.values().filter(idJornada=id,idVotante=idvotante)
        
        if candidato.exists() and jornadac.exists() and votante.exists() and not jornadav.exists(): #Verifica que todas las entidades existan
            jornadavotante = {
                'idJornadaVotante':str(id)+str(idvotante),
                'idVotante':idvotante,
                'idJornada':str(id),
                'idCandidato':idcandidato
            }

            jornadacandidatodb = Jornada_candidato.objects.get(idJornada=id,idCandidato=idcandidato)
            jornadacandidato = {
                'idJornadaCandidato':str(id)+str(idcandidato),
                'idJornada':str(id),
                'idCandidato':str(idcandidato),
            }

            jornadavotante_serializers = JornadaVotanteSerializer(data=jornadavotante)
            jornadacandidato_serializers = JornadaCandidatoSerializer(jornadacandidatodb,data=jornadacandidato)
            
            if jornadavotante_serializers.is_valid() and jornadacandidato_serializers.is_valid(): #Procesos de validación para los votos
                try:
                    jornadavotante_serializers.save()
                    jornadacandidato_serializers.save()
                    jsonresponse = {'code':'NE-200','message':'Success'}
                    return JsonResponse(jsonresponse,safe=False)
                except:
                    jsonresponse = {'code':'NE-500','message':'Lo siento. Algo salió mal'}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {'code':'NE-400','message':'Bad request'}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {'code':'NE-400','message':'Bad request'}
            return JsonResponse(jsonresponse,safe=False)