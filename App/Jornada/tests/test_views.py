import json
from django.test import TestCase, Client
from django.urls import reverse
from App.Jornada.models import Jornada, Jornada_candidato, Jornada_votante

class TestViewsJornada(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.urlGetJornada = reverse('jornadas:getJornada')

    def testGetJornadaMethodGetThenResponse200(self):
        response = self.client.get(self.urlGetJornada)
        self.assertEquals(response.status_code,200)

