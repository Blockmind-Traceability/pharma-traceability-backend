
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),

    path('api/v1/laboratories/', include('laboratory.urls')),

    path('api/v1/products/', include('product.urls')),

    path('api/v1/batches/', include('batch.urls')),


]
