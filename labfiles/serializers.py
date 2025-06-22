from rest_framework import serializers
from .models import LaboratoryFile

class LaboratoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaboratoryFile
        fields = ['id', 'name', 'file', 'uploaded_at']
