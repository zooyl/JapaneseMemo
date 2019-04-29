# django imports
import unittest
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

# app imports
from Hiragana.forms import UserAdvancedCreationForm
from Hiragana.models import Stats
from Hiragana.views import next_level_permission, streak_count, \
    streak_reset, add_attempts, exercise_completed

# library imports
import datetime


# Create your tests here.

class RegistrationViewTestCase(django.test.TestCase):

    def test_registration_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'auth/user_form.html')
        self.failUnless(isinstance(response.context['form'],
                                   UserAdvancedCreationForm))

    def test_registration_view_post_success(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test_username',
                                          'email': 'test@test.com',
                                          'password1': 'Mkonjibhu7!',
                                          'password2': 'Mkonjibhu7!'
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_registration_view_post_failure_password(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test_username',
                                          'email': 'test@test.com',
                                          'password1': 'pass_to_fail',
                                          'password2': 'mkonjibhu'
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_view_post_failure_mail(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test_username',
                                          'email': 'testmail',
                                          'password1': 'mkonjibhu',
                                          'password2': 'mkonjibhu'
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_registration_view_post_failure_username(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': '',
                                          'email': 'test@mail.com',
                                          'password1': 'mkonjibhu',
                                          'password2': 'mkonjibhu'
                                          }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_landing_page(self):
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        response = self.client.get(reverse("password_reset_done"))
        self.assertEqual(response.status_code, 200)

    def password_reset_complete(self):
        response = self.client.get(reverse("password_reset_complete"))
        self.assertEqual(response.status_code, 200)


class ConnectionRedirectTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_stats(self):
        response = self.client.get(reverse("stats"))
        self.assertEqual(response.status_code, 302)

    def test_easy(self):
        response = self.client.get(reverse("easy"))
        self.assertEqual(response.status_code, 302)

    def test_medium(self):
        response = self.client.get(reverse("medium"))
        self.assertEqual(response.status_code, 302)

    def test_hard(self):
        response = self.client.get(reverse("hard"))
        self.assertEqual(response.status_code, 302)

    def test_mixed(self):
        response = self.client.get(reverse("mixed"))
        self.assertEqual(response.status_code, 302)

    def test_diacritics(self):
        response = self.client.get(reverse("diacritics"))
        self.assertEqual(response.status_code, 302)


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


class PermissionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def tearDown(self):
        self.user.delete()

    def test_medium_level_permission(self):
        perm = Permission.objects.get(codename='medium_level')
        self.user.user_permissions.add(perm)
        self.assertTrue(self.user.has_perm('Hiragana.medium_level'))

    def test_hard_level_permission(self):
        perm = Permission.objects.get(codename='hard_level')
        self.user.user_permissions.add(perm)
        self.assertTrue(self.user.has_perm('Hiragana.hard_level'))

    def test_mixed_level_permission(self):
        perm = Permission.objects.get(codename='mixed_level')
        self.user.user_permissions.add(perm)
        self.assertTrue(self.user.has_perm('Hiragana.mixed_level'))

    def test_diacritics_permission(self):
        perm = Permission.objects.get(codename='diacritics')
        self.user.user_permissions.add(perm)
        self.assertTrue(self.user.has_perm('Hiragana.diacritics'))


class NextLevelPermissionFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_medium_level_function_permission(self):
        self.stats.completed = 5
        next_level_permission(self.stats)
        self.assertTrue(self.user.has_perm('Hiragana.medium_level'))

    def test_hard_level_function_permission(self):
        self.stats.completed = 10
        next_level_permission(self.stats)
        self.assertTrue(self.user.has_perm('Hiragana.hard_level'))

    def test_mixed_level_function_permission(self):
        self.stats.completed = 20
        next_level_permission(self.stats)
        self.assertTrue(self.user.has_perm('Hiragana.mixed_level'))

    def test_diacritics_function_permission(self):
        self.stats.completed = 15
        next_level_permission(self.stats)
        self.assertTrue(self.user.has_perm('Hiragana.diacritics'))


class StreakCountFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_streak_count_function(self):
        streak_count(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertAlmostEqual(self.stats.streak_timestamp, datetime.datetime.now(datetime.timezone.utc),
                               delta=datetime.timedelta(seconds=1))


class StreakResetFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_streak_reset_function(self):
        streak_reset(self.stats)
        self.assertEqual(self.stats.streak, 0)


class AddAttemptsFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_add_attempts_function(self):
        add_attempts(self.stats)
        self.assertEqual(self.stats.attempts, 1)


if __name__ == "__main__":
    unittest.main()
