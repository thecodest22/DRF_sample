from django.urls import path, include
from rest_framework import routers

from .views import ProductViewSet, UserViewSet


app_name = 'products'

router = routers.DefaultRouter()
# router.register('products', ProductViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
    # re_path(r'^products/$', ProductView.as_view(), name='products_api'),
