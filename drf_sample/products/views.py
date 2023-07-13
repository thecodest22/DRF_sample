from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        products_serialized = ProductSerializer(products, many=True)
        return Response(products_serialized.data)

    def post(self, request):
        # Логика обработки POST-запроса
        pass

    def put(self, request, pk):
        # Логика обработки PUT-запроса
        pass

    def delete(self, request, pk):
        # Логика обработки DELETE-запроса
        pass

