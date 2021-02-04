from django.test import SimpleTestCase
from django.urls import reverse, resolve
from App.Login import views

class TestUrls(SimpleTestCase):

    def testGetLoginUrl(self):
        url = reverse('login:getLogin')
        self.assertEquals(resolve(url).func,views.getLogin)