from django.contrib import admin
from customers.models.customer import Customer
from customers.models.order import Order
from customers.models.employee import Employee
from customers.models.item import Item
from customers.models.order_item import OrderItem

class CustomerAdmin(admin.ModelAdmin):
    def _queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
class EmployeeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
class ItemAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'total_price_in_cents')  # Display relevant fields in the list view

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # You might need to customize this further based on how OrderItems relate to users
        return qs.filter(order__customer__user=request.user)
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
