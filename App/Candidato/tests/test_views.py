import json
from datetime import datetime
from django.test import TestCase, Client
from django.urls import reverse
from App.Candidato import models, views

class TestViewJornada(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.nombreC1 = 'Nidia Asunción Cortéz Duarte'
        self.nombreC2 = 'Starbucks'
        self.initDate = "01/01/2021 09:00:00"
        self.finalDate = "02/01/2021 18:00:00"
        self.urlAllCandidatos = reverse('candidatos:getCandidato')
        self.urlCandidatosByID = reverse('candidatos:editCandidato',args=['idcandidato'])
        self.candidatos = []
        self.request = {
                "nombreCandidato": self.nombreC1,
                "propuestasGenerales": "Propuesta",
                "propuestaArchivo": "Propuesta archivo.pdf",
                "foto": "Foto.jpg ",
                "correoAdministrador": "administrador@administrador.ipn.mx"
            }

    def testGetIDCandidatoWithCompleteName(self):
        result = views.getidCandidato(self.nombreC1)
        self.assertEquals(len(result),11)
    
    def testGetIDCandidatoWithOneName(self):
        result = views.getidCandidato(self.nombreC2)
        self.assertEquals(len(result),11)
    
    def testConvertDateStringToDatetime(self):
        result = views.getDateFormat(self.initDate)
        self.assertEquals(type(result),datetime)

    def testMethodGETToGetAllCandidatos(self):
        response = self.client.get(self.urlAllCandidatos)
        self.assertEquals(response.status_code,200)

    def testMethodPOSTToCreateNewCandidato(self):
        response = self.client.post(self.urlAllCandidatos,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)

    def testMethodDELETEToEditACandidato(self):
        response = self.client.delete(self.urlCandidatosByID)
        self.assertEquals(response.status_code,200)   