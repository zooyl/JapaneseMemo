from django.db import models
from Hiragana.models import level


# Create your models here.


class Katakana(models.Model):
    sign = models.CharField(max_length=5)
    pronunciation = models.CharField(max_length=5)

    def __str__(self):
        return self.sign


class Levels(models.Model):
    preset = models.IntegerField(choices=level)
    memo = models.ForeignKey(Katakana, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.get_preset_display()
