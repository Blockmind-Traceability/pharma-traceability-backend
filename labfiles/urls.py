from django.urls import path
from .views import (
    LaboratoryFileUploadView,
    LaboratoryFileListView,
    LaboratoryFileDeleteView,
)

urlpatterns = [
    path('<int:laboratory_id>/files/', LaboratoryFileUploadView.as_view(), name='upload_files'),
    path('<int:laboratory_id>/files/list/', LaboratoryFileListView.as_view(), name='list_files'),
    path('files/<int:file_id>/delete/', LaboratoryFileDeleteView.as_view(), name='delete_file'),
]
