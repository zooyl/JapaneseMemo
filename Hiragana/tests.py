# django imports
import unittest
import django
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User, Permission

# app imports
from Hiragana.forms import UserAdvancedCreationForm
from Hiragana.models import Stats, Hiragana
from Hiragana.views import next_level_permission, streak_count, \
    streak_reset, add_attempts, exercise_completed, last_stamp_in_48_hours, \
    flag_true, flag_false, streak_once_a_day

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

    def test_registration_view_post_success_with_login(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test_username',
                                          'email': 'test@test.com',
                                          'password1': 'Mkonjibhu7!',
                                          'password2': 'Mkonjibhu7!'
                                          }, follow=True)
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'Welcome, test_username')

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
        streak_count(self.stats)
        self.assertEqual(self.stats.streak, 2)
        self.assertAlmostEqual(self.stats.streak_timestamp, datetime.datetime.now(datetime.timezone.utc),
                               delta=datetime.timedelta(seconds=1))


class StreakResetFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_streak_reset_function(self):
        self.stats.streak = 3
        streak_reset(self.stats)
        self.assertEqual(self.stats.streak, 1)


class AddAttemptsFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_add_attempts_function(self):
        self.assertEqual(self.stats.attempts, 0)
        add_attempts(self.stats)
        self.assertEqual(self.stats.attempts, 1)
        add_attempts(self.stats)
        self.assertEqual(self.stats.attempts, 2)


class ExerciseCompletedFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_exercise_completed(self):
        self.assertEqual(self.stats.attempts, 0)
        exercise_completed(self.stats)
        self.assertEqual(self.stats.completed, 1)
        exercise_completed(self.stats)
        self.assertEqual(self.stats.completed, 2)


class LastStampIn24HoursFunctionTest(unittest.TestCase):

    def test_stamp_in_less_than_48_first_time(self):
        self.user = User.objects.create_user(username='test_less_than_24', password='12345')
        self.stats = Stats.objects.create(user=self.user)
        self.client = Client()
        self.client.force_login(user=self.user)
        last_stamp_in_48_hours(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertEqual(self.stats.streak_flag, False)

    def test_stamp_in_less_than_48_second_time(self):
        self.user = User.objects.get(username="test_less_than_24")
        self.stats = Stats.objects.get(user=self.user)
        last_stamp_in_48_hours(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertEqual(self.stats.streak_flag, False)

    def test_stamp_in_more_than_48(self):
        self.user = User.objects.create_user(username='test_more_than_24', password='12345')
        self.stats = Stats.objects.create(user=self.user)
        two_days_ago = datetime.datetime.now() - datetime.timedelta(days=2)
        self.stats.streak_timestamp = two_days_ago
        self.stats.streak = 4
        self.stats.save()
        last_stamp_in_48_hours(self.stats)
        self.assertEqual(self.stats.streak, 1)


class FlagTrueFunctionTest(unittest.TestCase):

    def test_true(self):
        self.user = User.objects.create_user(username='test_flag_true', password='12345')
        self.stats = Stats.objects.create(user=self.user)
        self.stats.streak_flag = False
        self.stats.save()
        flag_true(self.stats)
        self.assertEqual(self.stats.streak_flag, True)


class FlagFalseFunctionTest(unittest.TestCase):

    def test_false(self):
        self.user = User.objects.create_user(username='test_flag_false', password='12345')
        self.stats = Stats.objects.create(user=self.user)
        self.stats.streak_flag = True
        self.stats.save()
        flag_false(self.stats)
        self.assertEqual(self.stats.streak_flag, False)


class StreakOnceADayFunctionTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_streak', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def tearDown(self):
        self.user.delete()

    def test_streak_two_times_same_day(self):
        streak_once_a_day(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertEqual(self.stats.streak_flag, False)
        streak_once_a_day(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertEqual(self.stats.streak_flag, False)

    def test_streak_next_day(self):
        streak_once_a_day(self.stats)
        self.assertEqual(self.stats.streak, 1)
        self.assertEqual(self.stats.streak_flag, False)
        today = datetime.datetime.now(datetime.timezone.utc)
        yesterday = today - datetime.timedelta(days=1, hours=1)
        self.stats.streak_timestamp = yesterday
        self.stats.save()
        streak_once_a_day(self.stats)
        self.assertEqual(self.stats.streak, 2)


class LandingPageTest(django.test.TestCase):

    def test_landing_page(self):
        client = Client()
        landing = client.get(reverse('landing-page'))
        self.assertEqual(landing.context['completed'], None)
        self.assertEqual(landing.context['attempts'], None)
        self.assertEqual(landing.context['signs'], 0)
        Hiragana.objects.create(sign="x", pronunciation="iks")
        self.user = User.objects.create_user(username='test_landing', password='12345')
        self.stats = Stats.objects.create(user=self.user)
        self.stats.completed = 5
        self.stats.attempts = 25
        self.stats.save()
        refresh = client.get(reverse('landing-page'))
        self.assertEqual(refresh.context['completed'], 5)
        self.assertEqual(refresh.context['attempts'], 25)
        self.assertEqual(refresh.context['signs'], 1)
        self.assertTemplateUsed(landing, 'landing_page.html')


class DashboardPageTest(django.test.TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_dashboard', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def test_logged_in_dashboard(self):
        self.client.force_login(self.user)
        dashboard = self.client.get(reverse('home'))
        self.assertEqual(dashboard.status_code, 200)
        self.assertTemplateUsed(dashboard, 'home.html')
        self.assertContains(dashboard, 'Welcome, test_dashboard')

    def test_not_authenticated_in_dashboard(self):
        dashboard = self.client.get(reverse('home'), follow=True)
        self.assertTemplateUsed(dashboard, 'registration/login.html')

    def test_not_authenticated_than_redirected_and_logged_in(self):
        dashboard = self.client.get(reverse('home'), follow=True)
        self.assertTemplateUsed(dashboard, 'registration/login.html')
        logging_in = self.client.post(reverse('login'),
                                      data={'username': 'test_dashboard',
                                            'password': '12345'}, follow=True)
        self.assertRedirects(logging_in, reverse('home'), status_code=302, target_status_code=200)
        self.assertTemplateUsed(logging_in, 'home.html')
        self.assertContains(logging_in, 'Welcome, test_dashboard')


class HiraganaPageTest(django.test.TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_hiragana', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def test_not_authenticated_user(self):
        response = self.client.get(reverse('hiragana'))
        self.assertRedirects(response, '/login/?hiragana=/home/hiragana', status_code=302, target_status_code=200)

    def test_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('hiragana'))
        self.assertTemplateUsed(response, 'hiragana.html')
        self.assertContains(response, 'List of unlocked levels')


class StatsPageTest(django.test.TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_stats', password='12345')
        self.stats = Stats.objects.create(user=self.user)

    def test_not_authenticated_user(self):
        response = self.client.get(reverse('stats'))
        self.assertRedirects(response, '/login/?stats=/stats/', status_code=302, target_status_code=200)

    def test_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('stats'))
        self.assertTemplateUsed(response, 'stats.html')
        self.assertContains(response, 'Your stats, test_stats')

    def test_with_0_stats(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('stats'))
        self.assertContains(response, 'id="test_comp" data-count="0"')
        self.assertContains(response, 'id="test_attempts" data-count="0"')
        self.assertContains(response, 'id="test_average" data-count=""')
        self.assertContains(response, 'id="test_streak" data-count="0"')

    def test_with_stats(self):
        stats = Stats.objects.get(user=self.user)
        stats.completed = 10
        stats.attempts = 52
        stats.streak = 3
        stats.save()
        self.client.force_login(self.user)
        response = self.client.get(reverse('stats'))
        self.assertContains(response, 'id="test_comp" data-count="10"')
        self.assertContains(response, 'id="test_attempts" data-count="52"')
        self.assertContains(response, 'id="test_average" data-count="5.2"')
        self.assertContains(response, 'id="test_streak" data-count="3"')


if __name__ == "__main__":
    unittest.main()
