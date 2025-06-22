from django.db import models
from laboratory.models import Laboratory  # Asegúrate que esta ruta sea correcta

class LaboratoryFile(models.Model):
    laboratory = models.ForeignKey(Laboratory, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='lab_documents/')
    name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.file.name
