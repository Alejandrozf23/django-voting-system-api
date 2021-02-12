import json
from django.test import TestCase, Client
from django.urls import reverse
from App.Login import views, models

class TestViewLogin(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.urlLogin = reverse('login:getLogin')
        self.urlRestartPassword = reverse('login:restartPassword')
        self.request = {
            "correo": "azepedaf1500@alumno.ipn.mx",
            "password":"742cecda27e58adcd22a8634743c6d1d7279fc1b4a57a88ff58087c1494f3c6f"
        }

    def testMethodPOSTToInitSession(self):
        response = self.client.post(self.urlLogin,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)
    
    def testMethodPUTToRestartPassword(self):
        response = self.client.put(self.urlRestartPassword,json.dumps(self.request),content_type="application/json")
        self.assertEquals(response.status_code,200)
    
    def testbuildPassword(self):
        response = views.buildPassword(12,'Alejandro Zepeda','azepedaf1500@alumno.ipn.mx')
        self.assertEquals(len(response),64)