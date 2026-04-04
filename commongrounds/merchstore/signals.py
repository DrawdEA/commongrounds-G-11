from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Transaction, Product


@receiver(post_save, sender=Transaction)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock = max(0, product.stock - instance.amount)
        if product.stock == 0:
            product.status = Product.Status.OUT_OF_STOCK
        product.save()
