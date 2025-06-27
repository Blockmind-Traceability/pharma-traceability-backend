from django.urls import path
from .views import (
    CreateBatchView,
    ListBatchView,
    RetrieveBatchView,
    RetrieveBatchBySerieView,
    UpdateBatchView,
    BatchDetailView,
    BatchBySerieView,
    BatchUpdateView,
    MyBatchListView
)

urlpatterns = [
    path('', CreateBatchView.as_view(), name='create_batch'),  # POST
    path('all/', ListBatchView.as_view(), name='list_batches'),  # GET
    path('<int:pk>/', RetrieveBatchView.as_view(), name='batch_detail'),  # GET by id
    path('series/<str:serie>/', RetrieveBatchBySerieView.as_view(), name='batch_by_serie'),  # GET by serie
    path('<int:pk>/edit/', UpdateBatchView.as_view(), name='update_batch'),  # PUT

    path('<int:id>/', BatchDetailView.as_view(), name='batch-detail'),
    path('by-serie/<str:serie_code>/', BatchBySerieView.as_view(), name='batch-by-serie'),
    path('<int:id>/update/', BatchUpdateView.as_view(), name='batch-update'),
    path('me/', MyBatchListView.as_view(), name='my-batches'),
]
