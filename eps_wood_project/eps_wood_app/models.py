from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Login(AbstractUser):
    usertype=models.CharField(max_length=50)
    viewpassword=models.CharField(max_length=50)

class Owner(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='owner/')
    status = models.CharField(max_length=20,choices=[('pending','Pending'),('approved','Approved'),('revoked','Revoked')],default='pending')

class Customer(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='customer/')
    status = models.CharField(max_length=20,choices=[('block','Block'),('unblock','Unblock')],default='unblock')

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('wood', 'Wood'),
        ('plywood', 'Plywood'),
        ('veneer', 'Veneer'),
    ]

    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    # Owner information
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    # Product basic details
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)

    # Specifications (optional based on product type)
    wood_type = models.CharField(max_length=100, blank=True, null=True)
    thickness = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)

    # Price & stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)  # e.g., cubic feet, sheet, piece
    stock_quantity = models.PositiveIntegerField()
    availability_status = models.CharField(max_length=20,choices=AVAILABILITY_CHOICES,default='in_stock')

    # Delivery
    delivery_available = models.BooleanField(default=False)
    delivery_charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # Control fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

class Cart(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('placed', 'Placed'),
            ('confirmed', 'Confirmed'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        default='placed'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cod', 'Cash on Delivery'),
            ('card', 'Card Payment'),
        ],
        default='cod'
    )
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Confirmed', 'Confirmed'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending'
    )

