from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Laboratory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="laboratory")
    business_name = models.CharField(max_length=100)
    nombre_comercial = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    representante_legal = models.CharField(max_length=100)
    dni_representante = models.CharField(max_length=20)
    tipo_productos = models.CharField(max_length=100)
    mercado_objetivo = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
