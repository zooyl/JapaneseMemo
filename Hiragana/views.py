from django.shortcuts import render
from django.views import View
from .forms import UserAdvancedCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Hiragana.models import Stats, Levels, Hiragana
from django.contrib.auth.models import User


# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


class Dashboard(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'home'

    def get(self, request):
        test = request.user
        stats = test.stats
        # stats = Stats.objects.get(test)
        # levels = Levels.objects.all()
        return render(request, "home.html", {'stats': stats})


class SignUp(CreateView):
    form_class = UserAdvancedCreationForm
    template_name = 'auth/user_form.html'
    success_url = reverse_lazy('landing-page')
