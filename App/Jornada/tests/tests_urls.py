from django.test import SimpleTestCase
from django.urls import reverse, resolve
from App.Jornada.views import getJornada, editJornada

class TestUrls(SimpleTestCase):

    def testGetJornadaUrl(self):
        url = reverse('jornadas:getJornada')
        self.assertEquals(resolve(url).func,getJornada)

    def testEditJornadaUrl(self):
        url = reverse('jornadas:editJornada',args=['idjornada'])
        self.assertEquals(resolve(url).func,editJornada)