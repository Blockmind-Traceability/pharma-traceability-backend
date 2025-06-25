from rest_framework import serializers
from .models import Batch, Series
from product.models import ProductUnit, Product
from product.serializers import ProductSerializer
from blockchain_client.services import register_event
from blockchain_client.models import BlockchainEvent, Responsible, Geolocation


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
        request = self.context.get('request')
        lab = request.user.laboratory
        series_data = validated_data.pop('series', [])
        batch = Batch.objects.create(**validated_data)

        for serial in series_data:
            try:
                product_unit = ProductUnit.objects.get(serial_number=serial)
                Series.objects.create(
                    batch=batch,
                    serie_code=serial,
                    product=product_unit.product
                )
                product_unit.batch = batch
                product_unit.save()

                # Crear evento shipment
                event = BlockchainEvent(
                    labId=str(lab.id),
                    eventType="shipment",
                    productSerial=serial,
                    batchId=str(batch.id),
                    origin=batch.origin,
                    destination=batch.destination,
                    currentLocation=batch.destination,
                    responsible=Responsible(
                        name=request.user.username,
                        role="lab",
                        entity=lab.business_name,
                        documentId=lab.dni_representante
                    ),
                    notes=f"Unidad serial {serial} agregada al lote #{batch.id}",
                    digitalSignature="FIRMA_AUTO",
                    deviceInfo="Sistema Django",
                    geolocation=Geolocation(
                        ip=self.get_client_ip(request),
                        lat=-12.0464,
                        lng=-77.0428
                    )
                )
                register_event(event)

            except ProductUnit.DoesNotExist:
                raise serializers.ValidationError(f"El número de serie '{serial}' no existe en ProductUnit.")
            except Exception as e:
                print(f"⚠️ Error al registrar evento shipment de {serial}: {e}")

        return batch

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '127.0.0.1')
    

class BatchDetailSerializer(serializers.ModelSerializer):
    series = SeriesSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'origin', 'destination', 'qr_code', 'created_at', 'series']
