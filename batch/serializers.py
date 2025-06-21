from rest_framework import serializers
from .models import Batch, Series

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'product', 'serie_code']

class BatchSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=True)

    class Meta:
        model = Batch
        fields = ['id', 'origin', 'destination', 'created_at', 'qr_code', 'is_editable', 'series']

    def create(self, validated_data):
        series_data = validated_data.pop('series')
        batch = Batch.objects.create(**validated_data)
        for serie in series_data:
            Series.objects.create(batch=batch, **serie)
        return batch

    def update(self, instance, validated_data):
        if not instance.is_editable:
            raise serializers.ValidationError("Este lote no puede ser editado.")

        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance
