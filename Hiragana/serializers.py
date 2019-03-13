from django.contrib.auth.models import User
from .models import Hiragana, Levels
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class HiraganaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hiragana
        fields = '__all__'


class LevelsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'
