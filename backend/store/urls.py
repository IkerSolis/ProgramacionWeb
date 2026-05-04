from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, KeyCodeViewSet, SaleViewSet, UserViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('keycodes', KeyCodeViewSet)
router.register('sales', SaleViewSet)
router.register('users', UserViewSet)

urlpatterns = router.urls
