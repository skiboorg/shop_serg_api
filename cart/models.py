from decimal import Decimal

from django.db import models

class Cart(models.Model):
    session_uuid = models.CharField(max_length=255, blank=True, null=True)

    @property
    def items_count(self):
        return self.items.all().count()

    @property
    def total_price(self):
        price = 0
        for item in self.items.all():
            price += Decimal(item.product.price) * item.amount
        return price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='items')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(default=0, blank=True, null=True)

    @property
    def total_price(self):
        price = Decimal(self.product.price) * self.amount
        return price