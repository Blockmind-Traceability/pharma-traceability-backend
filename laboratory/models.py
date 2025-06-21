from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Laboratory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="laboratory")
    business_name = models.CharField(max_length=100)
    ruc = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name

