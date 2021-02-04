from django.test import SimpleTestCase
from django.urls import reverse, resolve
from App.Votante import views

class TestUrls(SimpleTestCase):

    def testGetVotanteUrl(self):
        url = reverse('votantes:getVotante')
        self.assertEquals(resolve(url).func,views.getVotante)
    
    def testEditVotanteUrl(self):
        url = reverse('votantes:editVotante',args=['idvotante'])
        self.assertEquals(resolve(url).func,views.editVotante)