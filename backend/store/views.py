from rest_framework import viewsets
from .models import Product, KeyCode, Sale, User
from .serializers import ProductSerializer, KeyCodeSerializer, SaleSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .igdb import search_games, get_game_images
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    remember_me = request.data.get('remember_me', False)
    
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Expiración dinámica
        if remember_me:
            access.set_exp(lifetime=timedelta(days=14))
        else:
            access.set_exp(lifetime=timedelta(minutes=30))
            
        return Response({
            'token': str(access),
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        })
    else:
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

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
        if self.action in ['list', 'retrieve', 'images']:
            return [AllowAny()]
        return [IsAdminUser()]

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def images(self, request, pk=None):
        product = self.get_object()
        if product.igdb_id:
            images = get_game_images(product.igdb_id)
            # Agregar también el cover principal como primera imagen si existe
            cover_url = product.cover or product.image_url
            if cover_url and cover_url not in images:
                images.insert(0, cover_url)
        else:
            cover_url = product.cover or product.image_url
            images = [cover_url] if cover_url else []
        return Response(images)

class KeyCodeViewSet(viewsets.ModelViewSet):
    queryset = KeyCode.objects.all()

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_staff:
            from .serializers import KeyCodePrivateSerializer
            return KeyCodePrivateSerializer
        from .serializers import KeyCodeSerializer
        return KeyCodeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'platform', 'region', 'is_used']

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

    def create(self, request, *args, **kwargs):
        key_code_id = request.data.get('key_code')
        
        if not key_code_id:
            return Response({'error': 'Debes especificar un key_code válido para comprar.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Usamos transaction.atomic() para asegurar que toda la operación sea indivisible
        with transaction.atomic():
            try:
                # 2. select_for_update() bloquea la fila en la BD para evitar Race Conditions (múltiples compras simultáneas)
                keycode = KeyCode.objects.select_for_update().get(id=key_code_id)
            except KeyCode.DoesNotExist:
                return Response({'error': 'La llave no existe.'}, status=status.HTTP_404_NOT_FOUND)
            
            # 3. Verificamos que no haya sido comprada ya
            if keycode.is_used:
                return Response({'error': 'Esta llave ya fue vendida o se agotó el inventario.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # (Aquí iría la integración segura con Stripe/PayPal usando keycode.price como fuente de la verdad)
            
            # 4. Marcamos la llave como usada
            keycode.is_used = True
            keycode.save()

            # 5. Creamos la venta vinculada al usuario
            sale = Sale.objects.create(
                user=request.user,
                key_code=keycode,
                payment_method=request.data.get('payment_method', 'Credit Card')
            )
            
            # 6. Retornamos la llave ahora sí expuesta porque ya pagó por ella
            serializer = self.get_serializer(sale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        # Los usuarios comunes solo pueden interactuar con su propio registro
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
