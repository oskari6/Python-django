from rest_framework import serializers
from customers.models.order import Order
from customers.models.item import Item
from rest_framework import serializers
from .item_serializer import ItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)  # Nested serializer to include related items

    class Meta:
        model = Order
        fields = '__all__'

    # nested item creation
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(order=order, **item_data)
        return order