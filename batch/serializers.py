from rest_framework import serializers
from .models import Batch, Series
from product.models import ProductUnit

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ['id', 'product', 'serie_code']

class BatchSerializer(serializers.ModelSerializer):
    series = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Batch
        fields = ['id', 'origin', 'destination', 'qr_code', 'created_at', 'series']

    def create(self, validated_data):
        series_data = validated_data.pop('series', [])
        batch = Batch.objects.create(**validated_data)

        # Asignar ProductUnits
        ProductUnit.objects.filter(serial_number__in=series_data).update(batch=batch)

        return batch

    def update(self, instance, validated_data):
        if not instance.is_editable:
            raise serializers.ValidationError("Este lote no puede ser editado.")

        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance
