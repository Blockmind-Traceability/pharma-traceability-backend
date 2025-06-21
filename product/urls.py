from django.urls import path
from .views import (
    CreateProductView, ListProductView, RetrieveProductView, UpdateProductView
)

urlpatterns = [
    path('', CreateProductView.as_view(), name='create_product'),           # POST
    path('all/', ListProductView.as_view(), name='list_products'),          # GET
    path('<int:pk>/', RetrieveProductView.as_view(), name='get_product'),   # GET
    path('<int:pk>/edit/', UpdateProductView.as_view(), name='edit_product')# PUT
]
