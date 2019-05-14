# Lib imports
import random
import datetime

# Django imports
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission, User
from django.contrib.auth import login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator

# REST imports
from rest_framework import viewsets

# App imports
from .serializers import UserSerializer, HiraganaSerializer, LevelsSerializer
from .forms import UserAdvancedCreationForm
from Hiragana.models import Levels, Hiragana, Stats


# Views


def landing_page(request):
    signs = Hiragana.objects.count()
    completed = list(Stats.objects.aggregate(Sum('completed')).values())[0]
    attempts = list(Stats.objects.aggregate(Sum('attempts')).values())[0]
    return render(request, "landing_page.html",
                  {'completed': completed, 'attempts': attempts, 'signs': signs})


class Leaderboards(LoginRequiredMixin, View):

    def get(self, request):
        objects = Stats.objects.all().order_by('-completed', 'attempts', 'user')
        paginator = Paginator(objects, 8)
        page = request.GET.get('page')
        stat = paginator.get_page(page)
        return render(request, 'leaderboard.html', {'stat': stat})


class Dashboard(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "home.html")


class SignUp(CreateView):
    form_class = UserAdvancedCreationForm
    template_name = 'auth/user_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return valid


class EditProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = "profile.html"
    success_message = "Your account has been updated"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangeEmail(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['email']
    template_name = "registration/email_change.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return super(ChangeEmail, self).form_valid(form)
        form.add_error('email', f"{email} already exists")
        return super(ChangeEmail, self).form_invalid(form)


class ChangePassword(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'registration/password_change.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'registration/password_change.html', {'form': form})


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = Stats
    success_url = reverse_lazy('landing-page')

    def get_object(self, queryset=None):
        return self.request.user


class HiraganaMain(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "hiragana.html")


class StatsView(LoginRequiredMixin, View):

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
    if user.stats.completed == 25:
        perm = Permission.objects.get(codename='easy_katakana')
        user.user_permissions.add(perm)
    if user.stats.completed == 30:
        perm = Permission.objects.get(codename='medium_katakana')
        user.user_permissions.add(perm)
    if user.stats.completed == 35:
        perm = Permission.objects.get(codename='hard_katakana')
        user.user_permissions.add(perm)
    if user.stats.completed == 45:
        perm = Permission.objects.get(codename='mixed_katakana')
        user.user_permissions.add(perm)
    if user.stats.completed == 40:
        perm = Permission.objects.get(codename='diacritics_katakana')
        user.user_permissions.add(perm)
    return user


def streak_count(request):
    # Function count user day streak
    user = request.user
    user.stats.streak += 1
    return user.stats.save()


def streak_reset(request):
    # Function reset user day streak
    user = request.user
    user.stats.streak = 1
    return user.stats.save()


def flag_false(request):
    user = request.user
    user.stats.streak_flag = False
    return user.stats.save()


def flag_true(request):
    user = request.user
    user.stats.streak_flag = True
    return user.stats.save()


def streak_once_a_day(request):
    """
    Function is checking if 24 hours has passed since last
    time_stamp before setting flag to true and making streak again
    """
    user = User.objects.get(id=request.user.id)
    today = datetime.datetime.now(datetime.timezone.utc)
    last_stamp = user.stats.streak_timestamp
    time_delta = (today - last_stamp).total_seconds()
    hours = round(time_delta / 60 / 60, 2)
    if user.stats.streak_flag is True:
        streak_count(request)
        flag_false(request)
    elif user.stats.streak_flag is False:
        if hours > 24:
            flag_true(request)
            streak_once_a_day(request)


def last_stamp_in_48_hours(request):
    # Function checks if user did exercise in last 48 hours
    user = User.objects.get(id=request.user.id)
    today = datetime.datetime.now(datetime.timezone.utc)
    last_stamp = user.stats.streak_timestamp
    time_delta = (today - last_stamp).total_seconds()
    hours = round(time_delta / 60 / 60, 2)
    if 48 > hours >= 0:
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
    user.stats.streak_timestamp = datetime.datetime.now(datetime.timezone.utc)
    user.stats.save()
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
            last_stamp_in_48_hours(request)
            exercise_completed(request)
            request.session['points'] = 0
            next_level_permission(request)
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
            last_stamp_in_48_hours(request)
            exercise_completed(request)
            request.session['points'] = 0
            next_level_permission(request)
            return render(request, 'success.html')
        return redirect('mixed')
    sign = request.POST['sign']
    return render(request, 'answer-mixed.html', {'sign': sign, 'answer': answer,
                                                 'session': session})


# Levels

class PresetEasy(LoginRequiredMixin, View):

    def get(self, request):
        easy = Levels.objects.filter(preset=0)
        shuffle = random.sample(list(easy), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetMedium(LoginRequiredMixin, View):

    def get(self, request):
        medium = Levels.objects.filter(preset=1)
        shuffle = random.sample(list(medium), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetHard(LoginRequiredMixin, View):

    def get(self, request):
        hard = Levels.objects.filter(preset=2)
        shuffle = random.sample(list(hard), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetDiacritics(LoginRequiredMixin, View):

    def get(self, request):
        diacritics = Levels.objects.filter(preset=3)
        shuffle = random.sample(list(diacritics), 5)
        question = random.choice(shuffle)
        return render(request, "question.html", {'shuffle': shuffle, "question": question,
                                                 'points': request.session.get('points')})

    def post(self, request):
        return check_answer(request)


class PresetMixed(LoginRequiredMixin, View):

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
