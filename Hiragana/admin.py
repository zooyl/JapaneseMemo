from django.contrib import admin
import Hiragana.models

# Register your models here.

admin.site.register(Hiragana.models.Stats)
admin.site.register(Hiragana.models.Levels)
admin.site.register(Hiragana.models.Hiragana)
admin.site.register(Hiragana.models.Words)
admin.site.register(Hiragana.models.WordsLevels)
