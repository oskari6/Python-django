from customers.models.customer import Customer
from customers.serializers.customer_serializer import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def customers(request):
    if request.method == 'GET':
        data = Customer.objects.all()
        serializer = CustomerSerializer(data, many=True)
        return Response({'customers': serializer.data})
    
    elif request.method == 'POST':
        # adding the current user to the data
        data = request.data.copy()
        data['user'] = request.user.id
        
        serializer = CustomerSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def customer(request, id):
    try:
        customer_instance = Customer.objects.get(pk=id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomerSerializer(customer_instance)
        return Response({'customer': serializer.data})
    
    elif request.method == 'PATCH':
        serializer = CustomerSerializer(customer_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'customer': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)