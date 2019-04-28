import random

import datetime

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, User

from rest_framework import viewsets

from .serializers import UserSerializer, HiraganaSerializer, LevelsSerializer
from .forms import UserAdvancedCreationForm
from Hiragana.models import Levels, level, Hiragana, Stats


# Views

def landing_page(request):
    users = User.objects.count()
    signs = Hiragana.objects.count()
    completed = list(Stats.objects.aggregate(Sum('completed')).values())[0]
    attempts = list(Stats.objects.aggregate(Sum('attempts')).values())[0]
    return render(request, "landing_page.html",
                  {'completed': completed, 'users': users, 'attempts': attempts, 'signs': signs})


class Dashboard(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'home'

    def get(self, request):
        user = request.user
        stats = user.stats
        return render(request, "home.html", {'stats': stats, 'level': level})


class SignUp(CreateView):
    form_class = UserAdvancedCreationForm
    template_name = 'auth/user_form.html'
    success_url = reverse_lazy('landing-page')


class HiraganaMain(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'hiragana'

    def get(self, request):
        return render(request, "hiragana.html")


class StatsView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'stats'

    def get(self, request):
        user = request.user
        stats = Stats.objects.get(user=user)
        try:
            average = stats.attempts / stats.completed
            rounded = round(average, 2)
            return render(request, 'stats.html', {'stats': stats, 'average': rounded})
        except ZeroDivisionError:
            return render(request, 'stats.html', {'stats': stats})


# Functions

def next_level_permission(request):
    # Function to unlock next level for user
    user = request.user
    if user.stats.completed == 5:
        perm = Permission.objects.get(codename='medium_level')
        user.user_permissions.add(perm)
    if user.stats.completed == 10:
        perm = Permission.objects.get(codename='hard_level')
        user.user_permissions.add(perm)
    if user.stats.completed == 15:
        perm = Permission.objects.get(codename='diacritics')
        user.user_permissions.add(perm)
    if user.stats.completed == 20:
        perm = Permission.objects.get(codename='mixed_level')
        user.user_permissions.add(perm)
    return user


def streak_count(request):
    # Function count user day streak
    user = request.user
    user.stats.streak += 1
    user.stats.streak_timestamp = datetime.datetime.now(datetime.timezone.utc)
    user.stats.save()
    return user


def streak_reset(request):
    # Function reset user day streak
    user = request.user
    user.stats.streak = 0
    user.stats.save()
    return user


# determine flag to count streak
flag = True


def streak_once_a_day(request):
    """
    Function is checking if 24 hours has passed since last
    time_stamp before setting flag to true and checking for streak again
    """
    user = User.objects.get(id=request.user.id)
    today = datetime.datetime.now(datetime.timezone.utc)
    last_stamp = user.stats.streak_timestamp
    time_delta = (today - last_stamp).total_seconds()
    hours = round(time_delta / 60 / 60, 2)
    global flag
    if flag is True:
        streak_count(request)
        flag = False
    elif flag is False:
        if hours > 24:
            flag = True
            streak_once_a_day(request)


def last_login_in_24_hours(request):
    # Function checks if user was logged in last 24 hours
    user = User.objects.get(id=request.user.id)
    today = datetime.datetime.now(datetime.timezone.utc)
    time_delta = (today - user.last_login).total_seconds()
    hours = round(time_delta / 60 / 60, 2)
    if 24 > hours >= 0:
        streak_once_a_day(request)
    else:
        streak_reset(request)


def add_attempts(request):
    # Function counts user attempts
    user = request.user
    user.stats.attempts += 1
    user.stats.save()
    return user


def exercise_completed(request):
    # Function adds completed exercises and reset session
    user = request.user
    user.stats.completed += 1
    user.stats.save()
    request.session['points'] = 0
    return


def check_answer(request):
    # Function check if the answer is correct (in this case gives user points)
    # if there is not enough points, then redirect back where user came from
    # or if it's wrong, display correct answer
    session = request.session.get('points', 0)
    pronunciation = request.POST['pronunciation']
    answer = request.POST['answer']
    add_attempts(request)
    if pronunciation == answer:
        session += 1
        request.session['points'] = session
        if session >= 5:
            exercise_completed(request)
            next_level_permission(request)
            last_login_in_24_hours(request)
            return render(request, 'success.html')
        return redirect(request.get_full_path())
    sign = request.POST['sign']
    return render(request, 'answer.html', {'sign': sign, 'answer': answer,
                                           'session': session})


def check_answer_mixed(request):
    # Function check if the answer is correct (in this case gives user points)
    # if there is not enough points, then redirect back where user came from
    # or if it's wrong, display correct answer
    session = request.session.get('points', 0)
    pronunciation = request.POST['pronunciation']
    answer = request.POST['answer']
    add_attempts(request)
    if pronunciation == answer:
        session += 1
        request.session['points'] = session
        if session >= 10:
            exercise_completed(request)
            next_level_permission(request)
            last_login_in_24_hours(request)
            return render(request, 'success.html')
        return redirect('mixed')
    sign = request.POST['sign']
    return render(request, 'answer-mixed.html', {'sign': sign, 'answer': answer,
                                                 'session': session})


# Levels

class PresetEasy(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'easy'

    def get(self, request):
        easy = Levels.objects.filter(preset=0)
        shuffle = random.sample(list(easy), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetMedium(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'medium'

    def get(self, request):
        medium = Levels.objects.filter(preset=1)
        shuffle = random.sample(list(medium), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetHard(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'hard'

    def get(self, request):
        hard = Levels.objects.filter(preset=2)
        shuffle = random.sample(list(hard), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetDiacritics(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'diacritics'

    def get(self, request):
        diacritics = Levels.objects.filter(preset=3)
        shuffle = random.sample(list(diacritics), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetMixed(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'mixed'

    def get(self, request):
        mixed = Levels.objects.all()
        shuffle = random.sample(list(mixed), 5)
        question = random.choice(shuffle)
        return render(request, "mixed-question.html", {'shuffle': shuffle, "question": question,
                                                       'points': request.session.get('points')})

    def post(self, request):
        return check_answer_mixed(request)


# API VIEW

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class HiraganaViewSet(viewsets.ModelViewSet):
    queryset = Hiragana.objects.all().order_by('id')
    serializer_class = HiraganaSerializer


class LevelsViewSet(viewsets.ModelViewSet):
    queryset = Levels.objects.all().order_by('preset')
    serializer_class = LevelsSerializer
