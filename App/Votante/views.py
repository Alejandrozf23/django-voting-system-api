import json,sys,random,string
from hashlib import sha256
from datetime import date
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . import models
from . import serializers

def getallTipos():
    try:
        tipos = models.Tipo_Votante.objects.values()
        tipos_serializer = serializers.TipoVotanteSerializer(data=tipos)
        if tipos_serializer.is_valid:
            resulttipos = [entry for entry in tipos]
            return resulttipos
        else:
            return None
    except:
        return None

def buildPassword(length):
    password = ''.join(random.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for x in range(length))
    if not sendMail(password):
        return None
    passhash = sha256(password.encode('utf-8')).hexdigest()    
    return passhash

def sendMail(password):
    email = 'alexzepeda2908@gmail.com'
    return email

def buildNewVotante(votante):
    password = buildPassword(12)
    record = {
        'idVotante':votante['idVotante'],
        'nombreVotante':votante['nombreVotante'],
        'correoInstitucional':votante['correoInstitucional'],
        'correoAdministrador':votante['correoAdministrador'],
        'password':password if password != None else return {},
        'tipo':votante['tipo']
    }
    return record

def buildSavedVotante(votante):
    record = {
        'idVotante':votante['idVotante'],
        'nombreVotante':votante['nombreVotante'],
        'correoInstitucional':votante['correoInstitucional'],        
    }
    return record

def buildEditVotante(id,votante):
    edit = { 
        'idVotante':id,
        'nombreVotante':votante['nombreVotante'],
        'correoInstitucional':votante['correoInstitucional'],
        'password':models.Votante.objects.values().filter(idVotante=id)[0]['password'],
        'correoAdministrador':models.Votante.objects.values().filter(idVotante=id)[0]['correoAdministrador_id'],
        'tipo':models.Votante.objects.values().filter(idVotante=id)[0]['tipo_id']
    }
    return edit

def saveNewVotante(votante_serializer):
    try:
        votante_serializer.save()
        return True
    except:
        return False

def deleteVotante(votante):
    try:
        votante.delete()
        return True
    except:
        return False

def manageExceptionsVotantes(registrados):
    if len(registrados)>0:
        for i in range(len(registrados)):
            idvotante = registrados[i]['idVotante']
            votante = models.Votante.objects.get(idVotante=idvotante)
            deleteVotante(votante)

# Create your views here.
def getVotante(request):
    if request.method == 'GET': 
        votantes = models.Votante.objects.values() 
        votante_serializer = serializers.VotanteSerializer(data=votantes)
        if votante_serializer.is_valid: 
            requestjson = []
            list_result = [entry for entry in votantes]
            for i in range(len(list_result)): 
                record = { 
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
    
    if request.method == 'POST': 
        response = []
        nuevo_votante = JSONParser().parse(request)
        for i in range(len(nuevo_votante)):
            votante_serializer = serializers.VotanteSerializer(data=buildNewVotante(nuevo_votante[i]))
            if votante_serializer.is_valid():
                if not saveNewVotante(votante_serializer):
                    manageExceptionsVotantes(response)
                    jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                    return JsonResponse(jsonresponse,safe=False)
                response.append(buildSavedVotante(nuevo_votante[i]))
            else:
                manageExceptionsVotantes(response)
                jsonresponse = {"code":"NE-400","message":"Bad request"}
                return JsonResponse(jsonresponse,safe=False)
        return JsonResponse(response,safe=False)

def editVotante(request,id):
    if request.method == 'PUT':
        if models.Votante.objects.values().filter(idVotante=id).exists(): 
            votante = models.Votante.objects.get(idVotante=id) 
            edit_votante = JSONParser().parse(request)
            votante_serializer = serializers.VotanteSerializer(votante,data=buildEditVotante(id,edit_votante))
            if votante_serializer.is_valid():
                if saveNewVotante(votante_serializer):
                    jsonresponse = {"code":"NE-200","message":"Success"}
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
        if models.Votante.objects.values().filter(idVotante=id).exists(): 
            votante = models.Votante.objects.get(idVotante=id) 
            if deleteVotante(votante):
                jsonresponse = {"idVotante": id,"message":"Borrado con éxito"}
                return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
                return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)