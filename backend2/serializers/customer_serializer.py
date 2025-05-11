from rest_framework import serializers
from customers.models.customer import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        
    # I dont want the user handled by the front end (removed)    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)