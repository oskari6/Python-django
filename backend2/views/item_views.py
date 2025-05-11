from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from customers.models.item import Item
from customers.serializers.item_serializer import ItemSerializer

@api_view(['GET', 'POST'])
def items(request):
    if request.method == 'GET':
        data = Item.objects.all()
        serializer = ItemSerializer(data, many=True)
        return Response({'items': serializer.data})

    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'item': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def item(request, id):
    try:
        item_instance = Item.objects.get(pk=id)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item_instance)
        return Response({'item': serializer.data})

    elif request.method == 'PATCH':
        serializer = ItemSerializer(item_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'item': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        item_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)