import django
import os
import unittest
from django.test import Client
from django.urls import reverse

# Preparing environment for test purposes
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'JapaneseMemo.settings')
django.setup()
# Hiragana app models
from Hiragana.forms import UserAdvancedCreationForm
from Hiragana.models import Hiragana


# Create your tests here.


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_landing_page(self):
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_signup(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)


class UserCreationFormTest(unittest.TestCase):

    def test_form_valid(self):
        form = UserAdvancedCreationForm(data={'username': 'test2', 'password1': 'mkonjibhu',
                                              'password2': 'mkonjibhu', 'email': 'tester@mail.com'})
        self.assertTrue(form.is_valid())

    def test_form_password_invalid(self):
        form = UserAdvancedCreationForm(data={'username': 'test', 'password1': 'mko000',
                                              'password2': 'mk', 'email': 'tester@mail.com'})
        self.assertFalse(form.is_valid())

    def test_form_mail_invalid(self):
        form = UserAdvancedCreationForm(data={'username': 'test', 'password1': 'mkonjibhu',
                                              'password2': 'mkonjibhu', 'email': 'testermailwithoutat.com'})
        self.assertFalse(form.is_valid())


class HiraganaCreateTest(unittest.TestCase):

    def setUp(self):
        self.sign = Hiragana.objects.create(sign="test", pronunciation="ptest")

    def tearDown(self):
        self.sign.delete()

    def test_create_hiragana(self):
        self.assertIsInstance(self.sign, Hiragana)


if __name__ == "__main__":
    unittest.main()
