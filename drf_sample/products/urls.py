from django.urls import re_path, path, include
from rest_framework import routers

from .views import ProductView, UsersViewSet


app_name = 'products'

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^products/$', ProductView.as_view(), name='products_api'),
]
