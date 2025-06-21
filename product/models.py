from django.db import models
from laboratory.models import Laboratory

class Product(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    batch_number = models.CharField(max_length=50)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.batch_number}"
