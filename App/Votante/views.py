import json,sys,random,string
from hashlib import sha256
from datetime import date
from threading import Thread
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . import models
from . import serializers

class EmailThread(Thread):
    def __init__(self,email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

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

def buildPassword(length,user,email):
    password = ''.join(random.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for x in range(length))
    sendMail(password,user,email,'Nueva contraseña')
    passhash = getHashString(password)
    return passhash

def getHashString(message):
    return sha256(message.encode('utf-8')).hexdigest()

def sendMail(password,user,mail,asunto):
    context = {
        'user':user,
        'password':password,
        'host':settings.EMAIL_HOST_WEB
    }
    template = get_template('password_email.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        asunto,
        'TT2020-A060',
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(content,'text/html')
    EmailThread(email).start()

def buildNewVotante(votante):
    iduser = votante['idVotante']
    nombre = votante['nombreVotante']
    password = buildPassword(12,nombre,votante['correoInstitucional'])
    record = {
        'idVotante':iduser,
        'nombreVotante':nombre,
        'correoInstitucional':votante['correoInstitucional'],
        'correoAdministrador':votante['correoAdministrador'],
        'password':password,
        'tipo':votante['tipo'],
        'access_code':'012345',
        'jwtoken':None
    }
    return None if password == None else record

def buildSavedVotante(votante):
    record = {
        'idVotante':votante['idVotante'],
        'nombreVotante':votante['nombreVotante'],
        'correoInstitucional':votante['correoInstitucional'],        
    }
    return record

def updateVotante(idVotante,votanteUpdate):
    try:
        votanteDB = models.Votante.objects.get(idVotante = idVotante)
        votanteDB.nombreVotante = votanteUpdate['nombreVotante']
        votanteDB.correoInstitucional = votanteUpdate['correoInstitucional']
        votanteDB.save()
        return True
    except:
        return False

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
        votanteDB = models.Votante.objects.values().filter(idVotante=id)
        if votanteDB.exists(): 
            votanteRequest = JSONParser().parse(request)
            if updateVotante(id,votanteRequest):
                jsonresponse = {"code":"NE-200","message":"Success"}
                return JsonResponse(jsonresponse,safe=False)
            jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal"}
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