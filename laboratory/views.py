from rest_framework import generics, permissions
from .models import Laboratory
from .serializers import LaboratorySerializer, LaboratoryStatusSerializer
from .permissions import IsAdmin

# POST /api/v1/laboratories
class CreateLaboratoryView(generics.CreateAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]

# GET /api/v1/laboratories
class ListLaboratoriesView(generics.ListAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# GET /api/v1/laboratories/{id}
class RetrieveLaboratoryView(generics.RetrieveAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]

# PUT /api/v1/laboratories/{id}
class UpdateLaboratoryView(generics.UpdateAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]

# PUT /api/v1/laboratories/{id}/status
class UpdateLaboratoryStatusView(generics.UpdateAPIView):
    queryset = Laboratory.objects.all()
    serializer_class = LaboratoryStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'


