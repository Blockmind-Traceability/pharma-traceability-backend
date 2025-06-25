from rest_framework import generics, permissions
from .models import Laboratory
from .serializers import LaboratorySerializer, LaboratoryStatusSerializer
from .permissions import IsAdmin
from blockchain_client.services import create_genesis_block
from blockchain_client.models import GenesisBlock

# POST /api/v1/laboratories
class CreateLaboratoryView(generics.CreateAPIView):
    serializer_class = LaboratorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        laboratory = serializer.save(user=self.request.user)

        # Crear bloque génesis después de guardar el laboratorio
        genesis_data = GenesisBlock(
            labId=str(laboratory.id),
            business_name=laboratory.business_name,
            ruc=laboratory.ruc,
            representante_legal=laboratory.representante_legal,
            dni_representante=laboratory.dni_representante
        )
        try:
            create_genesis_block(genesis_data)
        except Exception as e:
            print(f"Error creando bloque génesis: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print("Detalle del error:", e.response.text)

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


