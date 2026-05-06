from django.db import models
from accounts.models import Profile


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'Available', 'Available'
        ON_SALE = 'On sale', 'On sale'
        OUT_OF_STOCK = 'Out of stock', 'Out of stock'

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    def __str__(self):
        if self.product_type:
            return f"{self.name} ({self.product_type.name})"
        return self.name

    class Meta:
        ordering = ['name']


class Transaction(models.Model):
    class Status(models.TextChoices):
        ON_CART = 'On cart', 'On cart'
        TO_PAY = 'To Pay', 'To Pay'
        TO_SHIP = 'To Ship', 'To Ship'
        TO_RECEIVE = 'To Receive', 'To Receive'
        DELIVERED = 'Delivered', 'Delivered'

    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ON_CART
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        buyer_name = self.buyer.display_name if self.buyer else 'Guest'
        return f"{buyer_name} — {self.product.name} x{self.amount}"

    class Meta:
        ordering = ['-created_on']
