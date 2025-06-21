from django.urls import path
from .views import (
    CreateBatchView,
    ListBatchView,
    RetrieveBatchView,
    RetrieveBatchBySerieView,
    UpdateBatchView
)

urlpatterns = [
    path('', CreateBatchView.as_view(), name='create_batch'),  # POST
    path('all/', ListBatchView.as_view(), name='list_batches'),  # GET
    path('<int:pk>/', RetrieveBatchView.as_view(), name='batch_detail'),  # GET by id
    path('series/<str:serie>/', RetrieveBatchBySerieView.as_view(), name='batch_by_serie'),  # GET by serie
    path('<int:pk>/edit/', UpdateBatchView.as_view(), name='update_batch'),  # PUT
]
