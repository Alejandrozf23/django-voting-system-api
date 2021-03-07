from App.Votante import models,serializers
from django.shortcuts import redirect
from django.conf import settings

# Create your views here.
def authAccount(request,id,token):
    if request.method == 'GET': 
        votante = models.Votante.objects.values().filter(idVotante=id)[0]
        if not votante['validate']:
            if token == votante['auth_token']:
                votanteDB = models.Votante.objects.get(idVotante=id)
                votanteDB.validate = True
                votanteDB.save()
        return redirect(settings.LOGIN)