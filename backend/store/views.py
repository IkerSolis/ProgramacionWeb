from rest_framework import viewsets
from .models import Product, KeyCode, Sale, User
from .serializers import ProductSerializer, KeyCodeSerializer, SaleSerializer, UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class KeyCodeViewSet(viewsets.ModelViewSet):
    queryset = KeyCode.objects.all()
    serializer_class = KeyCodeSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
