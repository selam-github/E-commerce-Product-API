from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet,UserViewSet,OrderViewSet,ReviewViewSet,ProductImageViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets
router.register(r'categories', CategoryViewSet)  # Registers Category viewset
router.register(r'products', ProductViewSet)     # Registers Product viewset
router.register(r'users', UserViewSet)           # Registers User viewset 
router.register(r'orders', OrderViewSet)         # Registers Order viewset
router.register(r'reviews', ReviewViewSet)       # Registers Review viewset
router.register(r'product-images', ProductImageViewSet)    #Rgister product-images viewset

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),   # DRF's router handles all registered ViewSets
]