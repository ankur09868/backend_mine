from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import authenticate
from .models import CustomUser



@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', CustomUser.EMPLOYEE)  # Default role to employee if not provided
        print("the role is:", role) 
        if not (username and email and password):
            return JsonResponse({'msg': 'Missing required fields'}, status=400)
        
        # Check if the username or email already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'msg': 'Username or email already exists'}, status=400)
        
        # Create a new user with the specified role
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        
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
            # Check user's role
            role = user.role
            # Implement your logic to determine which views to show based on the role
            # For example:
            if role == CustomUser.ADMIN:
                # Show admin views
                return Response({'msg': 'Login successful as admin'}, status=status.HTTP_200_OK)
            elif role == CustomUser.MANAGER:
                # Show manager views
                return Response({'msg': 'Login successful as manager'}, status=status.HTTP_200_OK)
            else:
                # Show employee views
                return Response({'msg': 'Login successful as employee'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)