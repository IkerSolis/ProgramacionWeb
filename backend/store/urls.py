from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, KeyCodeViewSet, SaleViewSet, UserViewSet
from django.urls import path
from .views import igdb_search

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('keycodes', KeyCodeViewSet, basename='keycode')
router.register('sales', SaleViewSet, basename='sale')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    *router.urls,
    path('igdb/search/', igdb_search, name='igdb-search'),
]
