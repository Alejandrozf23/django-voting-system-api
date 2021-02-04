from django.test import SimpleTestCase
from django.urls import reverse, resolve
from App.Candidato import views

class TestUrls(SimpleTestCase):

    def testGetCandidatoUrl(self):
        url = reverse('candidatos:getCandidato')
        self.assertEquals(resolve(url).func,views.getCandidato)

    def testEditCandidatoUrl(self):
        url = reverse('candidatos:editCandidato',args=['idcandidato'])
        self.assertEquals(resolve(url).func,views.editCandidato)