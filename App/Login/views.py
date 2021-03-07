import string,random
from hashlib import sha256
from threading import Thread
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from rest_framework.parsers import JSONParser
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from App.Administrador import models,serializers
from App.Votante.models import Votante,Tipo_Votante
from App.Votante.serializers import VotanteSerializer,TipoVotanteSerializer
from App.Jornada import models,serializers

class EmailThread(Thread):
    def __init__(self,email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

def getallTipos():
    try:
        tipos = Tipo_Votante.objects.values()
        tipos_serializer = TipoVotanteSerializer(data=tipos)
        if tipos_serializer.is_valid:
            resulttipos = [entry for entry in tipos]
            return resulttipos
        else:
            return None
    except:
        return None

def sendMailRestart(password,user,mail,asunto):
    context = {
        'user':user,
        'password':password
    }
    template = get_template('restart_password.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        asunto,
        'TT2020-A060',
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(content,'text/html')
    EmailThread(email).start()

def sendMailCode(pcode,user,mail,asunto):
    context = {
        'user':user,
        'code':code
    }
    template = get_template('code_email.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        asunto,
        'TT2020-A060',
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(content,'text/html')
    EmailThread(email).start()

def generateAccessCode(length,user,email):
    code = ''.join(random.choice(string.digits) for x in range(length))
    sendMailCode(code,user,email,'Código de acceso')
    return code

def buildPassword(length,user,email):
    password = ''.join(random.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for x in range(length))
    sendMailRestart(password,user,email,'Restauración de contraseña')
    passhash = sha256(password.encode('utf-8')).hexdigest()    
    return passhash

def restartPassword_Votante(votante):
    try:
        consult = Votante.objects.get(idVotante=votante['idVotante']) 
        consult.password = buildPassword(12,votante['nombreVotante'],votante['correoInstitucional'])
        consult.save()
        return True
    except:
        return False

def getJornadasByVotante(idvotante):
    votos = []
    jornadas = models.Jornada.objects.values()
    for i in range(len(jornadas)):
        idjornada = jornadas[i]['idJornada']
        jornadavotante = models.Jornada_votante.objects.values().filter(idJornada=idjornada,idVotante=idvotante)
        if jornadavotante.exists():                      
            votos.append({"idJornada":jornadas[i]['idJornada'],"nombreJornada":jornadas[i]['nombreJornada'],"voto":True})
        else:
            votos.append({"idJornada":jornadas[i]['idJornada'],"nombreJornada":jornadas[i]['nombreJornada'],"voto":False})
    return votos

# Create your views here.
def getLogin(request):
    if request.method == 'POST':
        loginuser = JSONParser().parse(request)
        email = loginuser['correo']
        password = loginuser['password']
        if email.split('@')[1].split('.')[0] == 'administrador':
            usuario = models.Administrador.objects.values().filter(emailadmin=email)
            if usuario.exists():
                if email==usuario[0]['emailadmin'] and password==usuario[0]['password']:
                    response = {
                        'correoAdministrador':usuario[0]['emailadmin'],
                        'permisos': usuario[0]['permisos']
                    }
                    return JsonResponse(response,safe=False)
                else:
                    jsonresponse = {'code':'NE-400','message':'Bad request'}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {'code':'NE-404','message':'Not found'}
                return JsonResponse(jsonresponse,safe=False)
        else:
            usuario = models.Votante.objects.values().filter(correoInstitucional=email)
            if usuario.exists():
                if email==usuario[0]['correoInstitucional'] and password==usuario[0]['password']:
                    consult = Votante.objects.get(idVotante=usuario[0]['idVotante'])
                    consult.access_code = generateAccessCode(6,usuario[0]['nombreVotante'],email)
                    consult.save()
                    jsonresponse = {'code':'NE-200','message':'Success'}
                    return JsonResponse(jsonresponse,safe=False)
                else:
                    jsonresponse = {'code':'NE-400','message':'Bad request'}
                    return JsonResponse(jsonresponse,safe=False)
            else:
                jsonresponse = {'code':'NE-404','message':'Not found'}
                return JsonResponse(jsonresponse,safe=False) 

def restartPassword(request):
    if request.method == 'PUT':
        email = JSONParser().parse(request)['correo']
        votante = models.Votante.objects.values().filter(correoInstitucional=email)
        if votante.exists():
            if restartPassword_Votante(votante[0]):
                jsonresponse = {"code":"NE-200","message":"Success"}
                return JsonResponse(jsonresponse,safe=False)
            jsonresponse = {"code":"NE-500","message":"Lo siento. Algo salió mal."}
            return JsonResponse(jsonresponse,safe=False)
        else:
            jsonresponse = {"code":"NE-404","message":"Not found"}
            return JsonResponse(jsonresponse,safe=False)

def accessCode(request):
    if request.method == 'POST':
        jsonrequest = JSONParser().parse(request)
        email = jsonrequest['correo']
        code = jsonrequest['codigo']
        usuario = models.Votante.objects.values().filter(correoInstitucional=email)[0]
        if usuario['access_code'] == code:
            idvotante = usuario['idVotante']
            response = {
                'idVotante':idvotante,
                'nombreVotante':usuario['nombreVotante'],
                'votos':getJornadasByVotante(idvotante)
            }
        else:
            response = {'code':'NE-400','message':'Bad request'}
        return JsonResponse(response,safe=False)