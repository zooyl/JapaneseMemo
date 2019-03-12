from django.shortcuts import render, redirect
from django.views import View
from .forms import UserAdvancedCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Hiragana.models import Levels, level
from django.contrib.auth.models import Permission
import random


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


class PresetEasy(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'easy'

    def get(self, request):
        easy = Levels.objects.filter(preset=0)
        shuffle = random.sample(list(easy), 5)
        question = random.choice(shuffle)
        return render(request, "easy.html", {'shuffle': shuffle, "question": question})

    def post(self, request):
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
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
                return redirect('home')
        return redirect('easy')


class PresetMedium(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'medium'

    def get(self, request):
        user = request.user
        if user.has_perm('Hiragana.medium_level'):
            medium = Levels.objects.filter(preset=1)
            shuffle = random.sample(list(medium), 5)
            question = random.choice(shuffle)
            return render(request, "medium.html", {'shuffle': shuffle, "question": question})
        return redirect('home')

    def post(self, request):
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
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
                return redirect('home')
        return redirect('medium')


class PresetHard(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'hard'

    def get(self, request):
        user = request.user
        if user.has_perm('Hiragana.hard_level'):
            hard = Levels.objects.filter(preset=2)
            shuffle = random.sample(list(hard), 5)
            question = random.choice(shuffle)
            return render(request, "hard.html", {'shuffle': shuffle, "question": question})
        return redirect('home')

    def post(self, request):
        pronunciation = request.POST['pronunciation']
        answer = request.POST['answer']
        if pronunciation == answer:
            points = request.session.get('points', 0)
            points += 1
            request.session['points'] = points
            if points >= 5:
                user = request.user
                user.stats.completed += 1
                user.stats.save()
                request.session['points'] = 0
                return redirect('home')
        return redirect('hard')
