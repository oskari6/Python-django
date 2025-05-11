from django.conf import settings
from rest_framework import serializers
from customers.models.employee import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'uuid', 'full_name', 'role','picture', 'picture_url']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_picture_url(self,obj):
        request = self.context.get('request')
        if obj.picture:
            if request:
                return request.build_absolute_uri(obj.picture.url)
            return f"{settings.MEDIA_URL}{obj.picture.url}"
        return None