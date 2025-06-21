from rest_framework import serializers
from .models import Laboratory

class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = '__all__'

class LaboratoryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ['status']

