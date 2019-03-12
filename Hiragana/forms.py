from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Hiragana.models import Stats


class UserAdvancedCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserAdvancedCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Stats.objects.create(user=user)
        return user
