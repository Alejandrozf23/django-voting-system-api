import json
from django.test import TestCase, Client
from django.urls import reverse
from App.Jornada import views, models

class TestViewJornada(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.initDate = "01/01/2021 09:00:00"
        self.finalDate = "02/01/2021 18:00:00"
        self.urlAllJornadas = reverse('jornadas:getJornada')
        self.urlJornadasByID = reverse('jornadas:editJornada',args=['idjornada'])
        self.candidatos = []
        self.request = {
                "nombreJornada": "Proceso de auscultacion",
                "fechaInicio": self.initDate,
                "fechaFinal": self.finalDate,
                "tipoJornada": "A",
                "correoAdministrador": "administrador@administrador.ipn.mx",
                "candidatos": self.candidatos
            }

    def testMethodGETToGetAllJornadas(self):
        response = self.client.get(self.urlAllJornadas)
        self.assertEquals(response.status_code,200)
    
    def testMethodGETToGetJornadaByID(self):
        response = self.client.get(self.urlJornadasByID)
        self.assertEquals(response.status_code,200)

    def testMethodPOSTToCreateNewJornadaWithoutCandidatos(self):
        response = self.client.post(self.urlAllJornadas,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)

    def testMethodPOSTToCreateNewJornadaWitCandidatos(self):
        self.candidatos.append('idcandidato')
        response = self.client.post(self.urlAllJornadas,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)

    def testMethodPUTToAddNewCandidato(self):
        self.candidatos.append('idcandidato')
        response = self.client.put(self.urlJornadasByID,json.dumps(self.candidatos),content_type="application/json")
        self.assertEquals(response.status_code,200)

    def testMethodDELETEToDeleteJornadaByID(self):
        response = self.client.delete(self.urlJornadasByID)
        self.assertEquals(response.status_code,200)

    def testGetIDJornadaWhenDateFormatIsCorrect(self):
        result = views.getidJornada(self.initDate,self.finalDate,'D')
        self.assertEquals(len(result),11)