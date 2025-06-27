from django.urls import path
from .views import (
    CreateLaboratoryView,
    ListLaboratoriesView,
    RetrieveLaboratoryView,
    UpdateLaboratoryView,
    UpdateLaboratoryStatusView,
    MyLaboratoryView,
    MyLaboratoryProductsView,
    
)

urlpatterns = [
    path('', CreateLaboratoryView.as_view(), name='create_laboratory'),  # POST
    path('all/', ListLaboratoriesView.as_view(), name='list_laboratories'),  # GET
    path('<int:pk>/', RetrieveLaboratoryView.as_view(), name='get_laboratory'),  # GET by id
    path('<int:pk>/status/', UpdateLaboratoryStatusView.as_view(), name='update_status'),  # PUT status
    path('<int:pk>/edit/', UpdateLaboratoryView.as_view(), name='update_laboratory'),  # PUT general

    path("me/", MyLaboratoryView.as_view(), name="my_laboratory"),
    path("me/products/", MyLaboratoryProductsView.as_view(), name="my_laboratory_products"),
]

