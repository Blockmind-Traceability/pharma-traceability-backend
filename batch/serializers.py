from rest_framework import serializers
from .models import Batch, Series
from product.models import ProductUnit, Product
from product.serializers import ProductSerializer


class SeriesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Series
        fields = ['id', 'serie_code', 'product']


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

        # Asociar ProductUnit con el batch y crear registro en Series
        for serial in series_data:
            try:
                product_unit = ProductUnit.objects.get(serial_number=serial)
                Series.objects.create(
                    batch=batch,
                    serie_code=serial,
                    product=product_unit.product  # asegurar que ProductUnit tenga un FK a Product
                )
                # Vincular ProductUnit al Batch si tiene el campo batch
                product_unit.batch = batch
                product_unit.save()
            except ProductUnit.DoesNotExist:
                raise serializers.ValidationError(f"El número de serie '{serial}' no existe en ProductUnit.")

        return batch

    def update(self, instance, validated_data):
        if hasattr(instance, 'is_editable') and not instance.is_editable:
            raise serializers.ValidationError("Este lote no puede ser editado.")

        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.save()
        return instance


class BatchDetailSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'origin', 'destination', 'qr_code', 'created_at', 'series']
