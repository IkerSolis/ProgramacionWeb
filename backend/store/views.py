from rest_framework import viewsets
from .models import Product, KeyCode, Sale, User
from .serializers import ProductSerializer, KeyCodeSerializer, SaleSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .igdb import search_games
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        })

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

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            from .serializers import KeyCodePrivateSerializer
            return KeyCodePrivateSerializer
        from .serializers import KeyCodeSerializer
        return KeyCodeSerializer

    
    def get_queryset(self):
        queryset = KeyCode.objects.all()
        product_id = self.request.query_params.get('product')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Sale.objects.all()
        return Sale.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAdminUser()]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        return [IsAdminUser()]
