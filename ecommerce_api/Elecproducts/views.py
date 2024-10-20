from django.shortcuts import render
from rest_framework import viewsets,permissions,status,filters
from .models import Category, Product,Order,Review,ProductImage
from django.contrib.auth.models import User
from .serializers import CategorySerializer, ProductSerializer,UserSerializer,OrderSerializer,ReviewSerializer,ProductImageSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend



# ViewSet for Category
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Only authenticated users can create, update, and delete products
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ViewSet for Product
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Only authenticated users can create, update, and delete products
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
    #  # Assign the product to the logged-in user who is creating it
        serializer.save(created_by=self.request.user)



     # Adding search and filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    

    # Define the available filters for the view
    filterset_fields = {
        'category': ['exact'],  # Filter by category ID
        'price': ['gte', 'lte'],  # Price range filtering (greater than or equal to, less than or equal to)
        'stock_quantity': ['gte'],  # Filter by available stock (greater than or equal to)
    }

    #searching by product name(partial matches)
    search_fields = ['name']  

    # Allow ordering by price or created date
    ordering_fields = ['price', 'created_date']  


# ViewSet for User       
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this   

#ViewSet for Order
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Create the order and reduce stock
        order = serializer.save(user=self.request.user)
        
        # Handle each order item
        for item in order.orderitem_set.all():
            product = item.product
            if product.stock_quantity < item.quantity:
                return Response({"detail": f"Not enough stock for {product.name}"}, status=status.HTTP_400_BAD_REQUEST)
            # Reduce stock
            product.stock_quantity -= item.quantity
            product.save()

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer     
