from django.db import models
from laboratory.models import Laboratory

class Product(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    registration_number = models.CharField(max_length=100)
    composition = models.CharField(max_length=255)
    presentation = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=100)
    storage_conditions = models.TextField()
    packaging = models.CharField(max_length=100)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='units')
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, related_name='units')
    serie = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Serie: {self.serie} ({self.product.name})"



