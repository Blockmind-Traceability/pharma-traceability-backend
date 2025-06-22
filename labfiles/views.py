from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import LaboratoryFile
from .serializers import LaboratoryFileSerializer
from laboratory.models import Laboratory

class LaboratoryFileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, laboratory_id):
        lab = get_object_or_404(Laboratory, id=laboratory_id)
        files = request.FILES.getlist('files')
        uploaded = []

        for f in files:
            doc = LaboratoryFile.objects.create(laboratory=lab, file=f, name=f.name)
            uploaded.append(doc)

        serializer = LaboratoryFileSerializer(uploaded, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LaboratoryFileListView(APIView):
    def get(self, request, laboratory_id):
        lab = get_object_or_404(Laboratory, id=laboratory_id)
        files = lab.files.all()
        serializer = LaboratoryFileSerializer(files, many=True)
        return Response(serializer.data)

class LaboratoryFileDeleteView(APIView):
    def delete(self, request, file_id):
        file = get_object_or_404(LaboratoryFile, id=file_id)
        file.file.delete(save=False)  # elimina físicamente
        file.delete()
        return Response({"message": "Archivo eliminado"}, status=status.HTTP_204_NO_CONTENT)
