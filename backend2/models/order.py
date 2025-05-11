from django.utils import timezone
from django.db import models
from .customer import Customer

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now)
    billing_address = models.CharField(max_length=500)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    region_code = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"
    
    def total_price_in_cents(self):
        return sum(item.total_price_in_cents for item in self.order_items.all())