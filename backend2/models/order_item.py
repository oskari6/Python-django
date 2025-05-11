from django.db import models
from .order import Order
from .item import Item

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price_in_cents(self):
        # Total price for this OrderItem is the item price multiplied by quantity
        return self.item.price_in_cents * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.item.item_name} for Order #{self.order.id}"