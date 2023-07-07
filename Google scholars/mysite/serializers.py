from rest_framework import serializers
from mysite.models import *


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model= Title
        fields = '__all__'
class AuthenSerializer(serializers.ModelSerializer):
    class Meta:
        model= Authen
        fields = '__all__'
