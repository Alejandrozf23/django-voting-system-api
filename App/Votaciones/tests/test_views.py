import json
from django.test import TestCase, Client
from django.urls import reverse
from App.Votaciones import views

class TestViewVotaciones(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.urlVotaciones = reverse('votaciones:getVotaciones',args=['idjornada'])
        self.request = {
            'idVotante':'2016601853',
            'idCandidato':'21SSS210213'
        }

    def testMethodGETToGetResultados(self):
        response = self.client.get(self.urlVotaciones)
        self.assertEquals(response.status_code,200)

    def testMethodPOSTToVotar(self):
        response = self.client.post(self.urlVotaciones,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)