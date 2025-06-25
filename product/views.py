from rest_framework import generics, permissions
from .models import Product, ProductUnit
from .serializers import ProductSerializer, ProductUnitSerializer
from .permissions import IsLaboratoryOwner
from laboratory.models import Laboratory
from blockchain_client.services import register_event
from blockchain_client.models import BlockchainEvent, Responsible, Geolocation
from django.utils.timezone import now

# POST /api/v1/products
class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lab = Laboratory.objects.get(user=self.request.user)
        serializer.save(laboratory=lab)

# GET /api/v1/products
class ListProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lab = Laboratory.objects.get(user=self.request.user)
        return lab.products.all()

# GET /api/v1/products/{id}
class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsLaboratoryOwner]

# PUT /api/v1/products/{id}
class UpdateProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsLaboratoryOwner]


class ProductUnitCreateView(generics.CreateAPIView):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_unit = serializer.save()

        try:
            lab = Laboratory.objects.get(user=self.request.user)

            event = BlockchainEvent(
                labId=str(lab.id),
                eventType="manufacture",
                productSerial=product_unit.serial_number,
                batchId="SIN_BATCH",  # Si se vincula luego a un lote, actualizar en otro evento
                origin="Planta de producción",
                destination="Almacén central",
                currentLocation="Almacén central",
                responsible=Responsible(
                    name=self.request.user.username,
                    role="lab",
                    entity=lab.business_name,
                    documentId=lab.dni_representante
                ),
                notes=f"Unidad serial {product_unit.serial_number} fabricada.",
                digitalSignature="FIRMA_AUTO",  # Puedes reemplazar por hash real más adelante
                deviceInfo="Sistema Django",
                geolocation=Geolocation(
                    ip=self.get_client_ip(),
                    lat=10, 
                    lng=10
                )
            )

            register_event(event)

        except Exception as e:
            print(f"Error al registrar evento blockchain: {e}")


    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')


class ProductUnitListView(generics.ListAPIView):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer


