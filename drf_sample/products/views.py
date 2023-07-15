from rest_framework import viewsets, permissions

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request):
    #     products = Product.objects.all()
    #     products_serialized = ProductSerializer(products, many=True)
    #     return Response(products_serialized.data)
    #
    # def post(self, request):
    #     # Логика обработки POST-запроса
    #     pass
    #
    # def put(self, request, pk):
    #     # Логика обработки PUT-запроса
    #     pass
    #
    # def delete(self, request, pk):
    #     # Логика обработки DELETE-запроса
    #     pass

