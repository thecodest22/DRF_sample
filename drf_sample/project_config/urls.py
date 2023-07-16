from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import viewsets, serializers, routers


urlpatterns = [
    path('', include('snippets.urls')),
    path('admin/', admin.site.urls),
    # path('products/', include('products.urls', namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest-framework')),
]
