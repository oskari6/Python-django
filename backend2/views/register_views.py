from django.http import JsonResponse
from customers.serializers.user_serializer import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth.transport import requests;
from google.oauth2 import id_token
from dotenv import load_dotenv
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(tokens, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
def google_auth(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))
            token = body.get("token")
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            
            email = id_info.get("email")
            first_name = id_info.get("given_name")
            last_name = id_info.get("family_name")
            
            user, created = User.objects.get_or_create(
                            email=email, 
                            defaults={"username": email, "first_name": first_name, "last_name": last_name}
                        )            
            # if created:
            #     serializer = UserSerializer(user)
                
            refresh = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return Response(tokens, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)
    