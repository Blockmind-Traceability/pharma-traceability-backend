from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsLaboratoryOwner
from laboratory.models import Laboratory

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

