from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),

    path('api/v1/laboratories/', include('laboratory.urls')),

    path('api/v1/products/', include('product.urls')),

    path('api/v1/batches/', include('batch.urls')),

    path('api/v1/laboratories-files/', include('labfiles.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

