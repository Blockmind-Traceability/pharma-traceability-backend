from django.urls import path

from .views import (
    CreateProductView, 
    ListProductView, 
    RetrieveProductView, 
    UpdateProductView, 
    ProductUnitListView, 
    ProductUnitCreateView, 
    TraceabilityBySeriesView,
    RegisterBlockchainEventView,
)

urlpatterns = [
    path('', CreateProductView.as_view(), name='create_product'),           # POST
    path('all/', ListProductView.as_view(), name='list_products'),          # GET
    path('<int:pk>/', RetrieveProductView.as_view(), name='get_product'),   # GET
    path('<int:pk>/edit/', UpdateProductView.as_view(), name='edit_product'),# PUT

    path('units/', ProductUnitListView.as_view(), name='unit-list'),
    path('units/create/', ProductUnitCreateView.as_view(), name='unit-create'),

    path('product-units/', ProductUnitListView.as_view(), name='list-product-units'),
    path('product-units/create/', ProductUnitCreateView.as_view(), name='create-product-unit'),

    path('traceability/<str:serie>/', TraceabilityBySeriesView.as_view(), name='traceability-by-series'),
    
    path('blockchain/events', RegisterBlockchainEventView.as_view(), name='register_blockchain_event'),



]
