from rest_framework import generics, permissions
from .models import Batch, Series
from .serializers import BatchSerializer
from laboratory.models import Laboratory
from .serializers import BatchDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateBatchView(generics.CreateAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lab = self.request.user.laboratory
        serializer.save(laboratory=lab)

class ListBatchView(generics.ListAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Batch.objects.filter(laboratory__email=self.request.user.email)

class RetrieveBatchView(generics.RetrieveAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class RetrieveBatchBySerieView(generics.RetrieveAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        serie_code = self.kwargs['serie']
        return Batch.objects.get(series__serie_code=serie_code)

class UpdateBatchView(generics.UpdateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]

class BatchDetailView(generics.RetrieveAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchDetailSerializer
    lookup_field = 'id'

class BatchBySerieView(APIView):
    def get(self, request, serie_code):
        serie = get_object_or_404(Series, serie_code=serie_code)
        batch = serie.batch
        serializer = BatchDetailSerializer(batch)
        return Response(serializer.data)

class BatchUpdateView(generics.UpdateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchDetailSerializer
    lookup_field = 'id'


class MyBatchListView(generics.ListAPIView):
    """List batches created by the authenticated user."""
    serializer_class = BatchDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Batch.objects.filter(laboratory__user=self.request.user)


