import json
from django.test import TestCase, Client
from django.urls import reverse
from App.Votante import views, models

class TestViewVotante(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.urlAllVotantes = reverse('votantes:getVotante')
        self.urlVotantesByID = reverse('votantes:editVotante',args=['idvotante'])
        self.request = [
            {
                "idVotante": "2016601853",
                "nombreVotante": "Alejandro de Jesús Zepeda Flores",
                "correoInstitucional": "azepedaf1500@alumno.ipn.mx",
                "correoAdministrador": "administrador@administrador.ipn.mx",
                "password":"password",
                'tipo':0
            },
            {
                "idVotante": "2016601854",
                "nombreVotante": "Ajitzi Ricardo Quintana Ruiz",
                "correoInstitucional": "aquintanar1600@alumno.ipn.mx",
                "correoAdministrador": "administrador@administrador.ipn.mx",
                "password":"password",
                'tipo':0
            }
        ]

    def testMethodGETToGetAllVotantes(self):
        response = self.client.get(self.urlAllVotantes)
        self.assertEquals(response.status_code,200)

    def testMethodPOSTToCreateNewVotante(self):
        response = self.client.post(self.urlAllVotantes,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)
    
    def testMethodPUTToEditVotante(self):
        response = self.client.put(self.urlVotantesByID,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)
    
    def testMethodDELETEToDeleteVotante(self):
        response = self.client.delete(self.urlVotantesByID)
        self.assertEquals(response.status_code,200)
    
    def testbuildPasswordUser(self):
        response = views.buildPassword(12,'user','email')
        self.assertEquals(len(response),64)