"""JapaneseMemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import Hiragana.views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', Hiragana.views.UserViewSet)
router.register('hiragana', Hiragana.views.HiraganaViewSet)
router.register('levels', Hiragana.views.LevelsViewSet)

urlpatterns = [
    path('last/', Hiragana.views.last_login_timedelta),
    path('api/', include(router.urls)),
    path('api-test/', include('rest_framework.urls', namespace="rest_framework")),
    path('admin/', admin.site.urls),
    path('', Hiragana.views.landing_page, name='landing-page'),
    path('signup/', Hiragana.views.SignUp.as_view(), name="signup"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('stats/', Hiragana.views.StatsView.as_view(), name='stats'),
    path('home/', Hiragana.views.Dashboard.as_view(), name='home'),
    path('home/easy', Hiragana.views.PresetEasy.as_view(), name='easy'),
    path('home/medium', Hiragana.views.PresetMedium.as_view(), name='medium'),
    path('home/hard', Hiragana.views.PresetHard.as_view(), name='hard'),
    path('home/mixed', Hiragana.views.PresetMixed.as_view(), name='mixed'),
    path('home/diacritics', Hiragana.views.PresetDiacritics.as_view(), name='diacritics'),
    path('home/hiragana', Hiragana.views.HiraganaMain.as_view(), name='hiragana'),
    path('password/reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password/reset/done', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password/reset/complete',
         PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('oauth/', include('social_django.urls', namespace='social')),
]
