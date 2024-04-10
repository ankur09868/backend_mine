from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import authenticate



@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not (username and email and password):
            return JsonResponse({'msg': 'Missing required fields'}, status=400)
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({'msg': 'Username or email already exists'}, status=400)
        
        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        return JsonResponse({'msg': 'User registered successfully'})
    else:
        return JsonResponse({'msg': 'Method not allowed'}, status=405)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        
        if not (username and password):
            return Response({'msg': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            # Implement your login logic here, for example, generating tokens
            return Response({'msg': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
