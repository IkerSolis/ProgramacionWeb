from rest_framework import viewsets
from .models import Product, KeyCode, Sale, User
from .serializers import ProductSerializer, KeyCodeSerializer, SaleSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .igdb import search_games

@api_view(['GET'])
@permission_classes([IsAdminUser])
def igdb_search(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Debes proporcionar un término de búsqueda'}, status=400)
    results = search_games(query)
    return Response(results)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class KeyCodeViewSet(viewsets.ModelViewSet):
    queryset = KeyCode.objects.all()
    serializer_class = KeyCodeSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAdminUser()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAdminUser()]
