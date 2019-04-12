from django.shortcuts import render, redirect
from django.views import View
from .forms import UserAdvancedCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, User
from Hiragana.models import Levels, level, Hiragana, Stats
import random
import datetime
from rest_framework import viewsets
from .serializers import UserSerializer, HiraganaSerializer, LevelsSerializer


# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


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
        user = request.user
        stats = user.stats
        users = User.objects.all().order_by('-stats__completed')
        return render(request, "hiragana.html", {'stats': stats, 'level': level,
                                                 'users': users})


class PresetEasy(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'easy'

    def get(self, request):
        points = request.session.get('points', 0)
        easy = Levels.objects.filter(preset=0)
        shuffle = random.sample(list(easy), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': points})

    def post(self, request):
        session = request.session.get('points')
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
        user = request.user
        user.stats.attempts += 1
        user.stats.save()
        if pronunciation == answer:
            points = request.session.get('points', 0)
            points += 1
            request.session['points'] = points
            if points >= 5:
                user = request.user
                user.stats.completed += 1
                user.stats.save()
                request.session['points'] = 0
                if user.stats.completed == 5:
                    perm = Permission.objects.get(codename='medium_level')
                    user.user_permissions.add(perm)
                return redirect('hiragana')
            return redirect('easy')
        sign = request.POST['sign']
        return render(request, 'answer.html', {'sign': sign, 'answer': answer,
                                               'session': session})


class PresetMedium(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'medium'

    def get(self, request):
        user = request.user
        if user.has_perm('Hiragana.medium_level'):
            points = request.session.get('points', 0)
            medium = Levels.objects.filter(preset=1)
            shuffle = random.sample(list(medium), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': points})
        return redirect('hiragana')

    def post(self, request):
        session = request.session.get('points')
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
        user = request.user
        user.stats.attempts += 1
        user.stats.save()
        if pronunciation == answer:
            points = request.session.get('points', 0)
            points += 1
            request.session['points'] = points
            if points >= 5:
                user = request.user
                user.stats.completed += 1
                user.stats.save()
                request.session['points'] = 0
                if user.stats.completed == 10:
                    perm = Permission.objects.get(codename='hard_level')
                    user.user_permissions.add(perm)
                return redirect('hiragana')
            return redirect('medium')
        sign = request.POST['sign']
        return render(request, 'answer.html', {'sign': sign, 'answer': answer,
                                               'session': session})


class PresetHard(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'hard'

    def get(self, request):
        user = request.user
        if user.has_perm('Hiragana.hard_level'):
            points = request.session.get('points', 0)
            hard = Levels.objects.filter(preset=2)
            shuffle = random.sample(list(hard), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': points})
        return redirect('hiragana')

    def post(self, request):
        session = request.session.get('points')
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
        user = request.user
        user.stats.attempts += 1
        user.stats.save()
        if pronunciation == answer:
            points = request.session.get('points', 0)
            points += 1
            request.session['points'] = points
            if points >= 5:
                user = request.user
                user.stats.completed += 1
                user.stats.save()
                request.session['points'] = 0
                if user.stats.completed == 15:
                    perm = Permission.objects.get(codename='mixed_level')
                    user.user_permissions.add(perm)
                return redirect('hiragana')
            return redirect('hard')
        sign = request.POST['sign']
        return render(request, 'answer.html', {'sign': sign, 'answer': answer,
                                               'session': session})


class PresetMixed(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'mixed'

    def get(self, request):
        user = request.user
        if user.has_perm('Hiragana.mixed_level'):
            points = request.session.get('points', 0)
            mixed = Levels.objects.all()
            shuffle = random.sample(list(mixed), 5)
            question = random.choice(shuffle)
            return render(request, "mixed-question.html", {'shuffle': shuffle, "question": question,
                                                           'points': points})
        return redirect('hiragana')

    def post(self, request):
        session = request.session.get('points')
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
        user = request.user
        user.stats.attempts += 1
        user.stats.save()
        if pronunciation == answer:
            points = request.session.get('points', 0)
            points += 1
            request.session['points'] = points
            if points >= 10:
                user = request.user
                user.stats.completed += 1
                user.stats.save()
                request.session['points'] = 0
                if user.stats.completed == 20:
                    perm = Permission.objects.get(codename='diacritics')
                    user.user_permissions.add(perm)
                return redirect('hiragana')
            return redirect('mixed')
        sign = request.POST['sign']
        return render(request, 'answer-mixed.html', {'sign': sign, 'answer': answer,
                                                     'session': session})


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
