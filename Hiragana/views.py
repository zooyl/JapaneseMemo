from django.shortcuts import render
from .forms import UserAdvancedCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


# Create your views here.

def landing_page(request):
    return render(request, "landing_page.html")


class SignUp(CreateView):
    form_class = UserAdvancedCreationForm
    template_name = 'auth/user_form.html'
    success_url = reverse_lazy('landing-page')
