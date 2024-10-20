from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product,Order,OrderItem,Review,ProductImage

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a user with a hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        # Update the user's info and password if provided
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
    def validate_password(self, value):
        # Custom validation logic for the password
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    

# category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_date', 'updated_date']


#  product serializer
class ProductSerializer(serializers.ModelSerializer):
    # To display category data in product
    category = CategorySerializer(read_only=True) 

    # Used to assign the category by ID while creating/updating
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )  
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 'stock_quantity', 'image_url', 'created_date', 'updated_date', 'created_by']
        read_only_fields = ['created_by', 'created_date', 'updated_date']

    # Field-level validation for name
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value
    
    # Field-level validation for price
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value
    
    # Field-level validation for stock quantity
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
    
#OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

#Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_items', 'total_price', 'created_at']
        read_only_fields = ['user', 'total_price', 'created_at']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        
        # Create order items and reduce stock
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order 
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'user', 'rating', 'review_content', 'created_at']
        read_only_fields = ['created_at','review_content', 'created_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product', 'image_url', 'uploaded_at']
        read_only_fields = ['uploaded_at']   