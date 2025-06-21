from django.db import models
from laboratory.models import Laboratory
from product.models import Product

class Batch(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='batches')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return f"Lote #{self.id} - {self.origin} → {self.destination}"

class Series(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='series')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    serie_code = models.CharField(max_length=100, unique=True)


