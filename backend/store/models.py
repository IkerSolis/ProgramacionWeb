import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    igdb_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=200)
    cover = models.URLField(max_length=500, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class KeyCode(models.Model):

    class Platform(models.TextChoices):
        PC = 'PC', 'PC'
        PLAYSTATION = 'PlayStation', 'PlayStation'
        XBOX = 'Xbox', 'Xbox'
        NINTENDO = 'Nintendo', 'Nintendo'

    class Region(models.TextChoices):
        GLOBAL = 'Global', 'Global'
        MX = 'MX', 'MX'
        US = 'US', 'US'
        EU = 'EU', 'EU'
        ASIA = 'Asia', 'Asia'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    key = models.CharField(max_length=200)
    is_used = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    platform = models.CharField(
        max_length=20,
        choices=Platform.choices,
        default=Platform.PC,
    )
    region = models.CharField(
        max_length=20,
        choices=Region.choices,
        default=Region.GLOBAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.key}"

class Sale(models.Model):

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'Credit Card', 'Credit Card'
        DEBIT_CARD = 'Debit Card', 'Debit Card'
        PAYPAL = 'PayPal', 'PayPal'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key_code = models.OneToOneField(KeyCode, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CREDIT_CARD,
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.key_code}"

    
