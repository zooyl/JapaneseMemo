from django.test import TestCase
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

# app imports
from Hiragana.models import Stats


# Create your tests here.

class PresetsTests(django.test.TestCase):
    fixtures = ['Katakana.json', 'Katakana_Levels.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_preset', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def test_preset_easy(self):
        self.client.force_login(self.user)
        self.client.get(reverse('kata_easy'))
        self.assertTemplateUsed('question.html')

    def test_preset_medium_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_medium'))
        self.assertTemplateUsed('error.html')
        self.assertContains(response, "<p>Not so fast</p>")
        self.assertContains(response, "You don&#39;t have permission to visit this page")

    def test_preset_medium_with_permission(self):
        perm = Permission.objects.get(codename='medium_katakana')
        self.user.user_permissions.add(perm)
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_medium'))
        self.assertTemplateUsed('question.html')
        self.assertContains(response, "Points:")
        self.assertContains(response, "Pronunciation:")

    def test_preset_hard_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_hard'))
        self.assertTemplateUsed('error.html')
        self.assertContains(response, "<p>Not so fast</p>")
        self.assertContains(response, "You don&#39;t have permission to visit this page")

    def test_preset_hard_with_permission(self):
        perm = Permission.objects.get(codename='hard_katakana')
        self.user.user_permissions.add(perm)
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_hard'))
        self.assertTemplateUsed('question.html')
        self.assertContains(response, "Points:")
        self.assertContains(response, "Pronunciation:")

    def test_preset_diacritics_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_diacritics'))
        self.assertTemplateUsed('error.html')
        self.assertContains(response, "<p>Not so fast</p>")
        self.assertContains(response, "You don&#39;t have permission to visit this page")

    def test_preset_diacritics_with_permission(self):
        perm = Permission.objects.get(codename='diacritics_katakana')
        self.user.user_permissions.add(perm)
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_diacritics'))
        self.assertTemplateUsed('question.html')
        self.assertContains(response, "Points:")
        self.assertContains(response, "Pronunciation:")

    def test_preset_mixed_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_mixed'))
        self.assertTemplateUsed('error.html')
        self.assertContains(response, "<p>Not so fast</p>")
        self.assertContains(response, "You don&#39;t have permission to visit this page")

    def test_preset_mixed_with_permission(self):
        perm = Permission.objects.get(codename='mixed_katakana')
        self.user.user_permissions.add(perm)
        self.client.force_login(self.user)
        response = self.client.get(reverse('kata_mixed'))
        self.assertTemplateUsed('question.html')
        self.assertContains(response, "Points:")
        self.assertContains(response, "Pronunciation:")


class KatakanaPageTest(django.test.TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_katakana', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def test_not_authenticated_user(self):
        response = self.client.get(reverse('katakana'))
        self.assertRedirects(response, '/login/?next=/home/katakana', status_code=302, target_status_code=200)

    def test_authenticated_user_without_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('katakana'))
        self.assertTemplateUsed('error.html')
        self.assertContains(response, "<p>Not so fast</p>")
        self.assertContains(response, "You don&#39;t have permission to visit this page")

    def test_authenticated_user_with_permission(self):
        perm = Permission.objects.get(codename='easy_katakana')
        self.user.user_permissions.add(perm)
        self.client.force_login(self.user)
        response = self.client.get(reverse('katakana'))
        self.assertTemplateUsed(response, 'katakana.html')
        self.assertContains(response, 'List of unlocked levels')
