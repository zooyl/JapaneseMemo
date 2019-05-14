from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.

class KatakanaMain(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm('Hiragana.easy_katakana'):
            return render(request, "katakana.html")
        messages.error(request, "You don't have permission to visit this page")
        return render(request, 'error.html')
