# Lib imports
import random

# Django imports
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Hiragana imports
from Hiragana.views import check_answer, check_answer_mixed

# App imports
import Katakana.models


# Create your views here.

class KatakanaMain(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.easy_katakana'):
            return render(request, "katakana.html")
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')


# Levels


class PresetEasy(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.easy_katakana'):
            easy = Katakana.models.Levels.objects.filter(preset=0)
            shuffle = random.sample(list(easy), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': request.session.get('points')})
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')

    def post(self, request):
        return check_answer(request)


class PresetMedium(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.medium_katakana'):
            medium = Katakana.models.Levels.objects.filter(preset=1)
            shuffle = random.sample(list(medium), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': request.session.get('points')})
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')

    def post(self, request):
        return check_answer(request)


class PresetHard(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.hard_katakana'):
            hard = Katakana.models.Levels.objects.filter(preset=2)
            shuffle = random.sample(list(hard), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': request.session.get('points')})
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')

    def post(self, request):
        return check_answer(request)


class PresetDiacritics(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.diacritics_katakana'):
            diacritics = Katakana.models.Levels.objects.filter(preset=3)
            shuffle = random.sample(list(diacritics), 5)
            question = random.choice(shuffle)
            return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                     'points': request.session.get('points')})
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')

    def post(self, request):
        return check_answer(request)


class PresetMixed(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.mixed_katakana'):
            mixed = Katakana.models.Levels.objects.all()
            shuffle = random.sample(list(mixed), 5)
            question = random.choice(shuffle)
            return render(request, "mixed-question.html", {'shuffle': shuffle, "question": question,
                                                           'points': request.session.get('points')})
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')

    def post(self, request):
        return check_answer_mixed(request)
