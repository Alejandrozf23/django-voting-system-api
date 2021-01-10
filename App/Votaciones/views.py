from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from App.Candidato.models import Candidato
from App.Candidato.serializers import CandidatoSerializer
from App.Votante.models import Votante
from App.Votante.serializers import VotanteSerializer
from App.Jornada.models import Jornada_votante,Jornada,Jornada_candidato
from App.Jornada.serializers import JornadaVotanteSerializer,JornadaCandidatoSerializer,JornadaSerializer

# Create your views here.
def getVotaciones(request,id):
    if request.method == 'GET':
        total = []
        votosT = Jornada_candidato.objects.values().filter(idJornada=id)
        for i in range(len(votosT)): #Ciclo para votos totales
            record = {
                'nombreCandidato':Candidato.objects.values().filter(idCandidato=votosT[i]['idCandidato_id'])[0]['nombreCandidato'],
                'novotos':votosT[i]['novotos']
            }
            total.append(record)
        votosP = Jornada_votante.objects.values().filter(idJornada=id).order_by('-idCandidato')
        auxiliar = []
        candidatosAlumnos = []
        candidatosProfesor = [] 
        candidatosPAAE = []
        for i in range(len(votosT)):
            nombre = Candidato.objects.values().filter(idCandidato=votosT[i]['idCandidato_id'])[0]['nombreCandidato']
            if not nombre in auxiliar:
                auxiliar.append(nombre)
                candidatosAlumnos.append({'nombreCandidato':nombre,'novotos':0})
                candidatosProfesor.append({'nombreCandidato':nombre,'novotos':0})
                candidatosPAAE.append({'nombreCandidato':nombre,'novotos':0})

        for i in range(len(votosP)):
            idcandidato = votosP[i]['idCandidato_id']
            idvotante = votosP[i]['idVotante_id']
            nombre = Candidato.objects.values().filter(idCandidato=idcandidato)[0]['nombreCandidato']
            tipovotante = Votante.objects.values().filter(idVotante=idvotante)[0]['tipo_id']
            if tipovotante == 0:
                for j in range(len(candidatosAlumnos)):
                    if candidatosAlumnos[j]['nombreCandidato'] == nombre:
                        candidatosAlumnos[j]['novotos'] += 1
            elif tipovotante == 1:
                for j in range(len(candidatosProfesor)):
                    if candidatosProfesor[j]['nombreCandidato'] == nombre:
                        candidatosProfesor[j]['novotos'] += 1
            elif tipovotante == 2:
                for j in range(len(candidatosPAAE)):
                    if candidatosPAAE[j]['nombreCandidato'] == nombre:
                        candidatosPAAE[j]['novotos'] += 1
        parcial = [
            {'tipo':'alumnos','votos':candidatosAlumnos},
            {'tipo':'profesores','votos':candidatosProfesor},
            {'tipo':'PAAE','votos':candidatosPAAE}
        ]
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
                'idJornada':id,
                'idCandidato':idcandidato
            }

            jornadacandidatodb = Jornada_candidato.objects.get(idJornada=id,idCandidato=idcandidato)
            votos = (Jornada_candidato.objects.values().filter(idJornada=id,idCandidato=idcandidato)[0]['novotos'])+1
            jornadacandidato = {
                'idJornadaCandidato':str(id)+str(idcandidato),
                'idJornada':str(id),
                'idCandidato':str(idcandidato),
                'novotos':votos
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