from django.db import models
from django.contrib.auth.models import User

# Create your models here.

level = (
    (0, 'Easy'),
    (1, 'Medium'),
    (2, 'Hard'),
    (3, 'Diacritics'),
)


class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    streak_timestamp = models.DateTimeField(auto_now_add=True)
    streak_flag = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        permissions = (
            ('medium_level', "Can start medium level"),
            ('hard_level', "Can start hard level"),
            ('mixed_level', "Can start mixed level"),
            ('diacritics', "Can start diacritics level"),
            ('easy_katakana', "Can start easy katakana level"),
            ('medium_katakana', "Can start medium katakana level"),
            ('hard_katakana', "Can start hard katakana level"),
            ('mixed_katakana', "Can start mixed katakana level"),
            ('diacritics_katakana', "Can start diacritics katakana level"),
        )


class Hiragana(models.Model):
    sign = models.CharField(max_length=5)
    pronunciation = models.CharField(max_length=5)

    def __str__(self):
        return self.sign


class Levels(models.Model):
    preset = models.IntegerField(choices=level)
    memo = models.ForeignKey(Hiragana, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.get_preset_display()
