from django.test import SimpleTestCase
from django.urls import reverse, resolve
from App.Votaciones import views

class TestUrls(SimpleTestCase):

    def testEditCandidatoUrl(self):
        url = reverse('votaciones:getVotaciones',args=['idjornada'])
        self.assertEquals(resolve(url).func,views.getVotaciones)