from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True,null=True)
    slug=models.SlugField(unique=True) #a slug is a URL of the category name which is  useful for SEO
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField(max_length=500, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name  
    
    # clean methode or validation 
    def clean(self):   
        # Validation for name
        if not self.name:
            raise ValidationError("Name cannot be empty.")
        if len(self.name) < 3:
            raise ValidationError("Name must be at least 3 characters long.")

        # Validation for price
        if self.price <= 0:
            raise ValidationError("Price must be greater than 0.")

        # Validation for stock quantity
        if self.stock_quantity < 0:
            raise ValidationError("Stock quantity cannot be negative.")

    def save(self, *args, **kwargs):
        self.clean()  # Ensure validation is called before saving the object
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
# Order model
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
# OrderItem model 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Check if there is enough stock
        if self.product.stock_quantity < self.quantity:
            raise ValidationError(f"Not enough stock for {self.product.name}. Only {self.product.stock_quantity} left.")
        
        # Reduce the stock quantity
        self.product.stock_quantity -= self.quantity
        self.product.save()
        
        super().save(*args, **kwargs) 


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  
    review_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.rating} stars'
     


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} Image'