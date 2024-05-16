from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Import other necessary modules as needed...

# Endpoint to retrieve user details by username
@csrf_exempt
def get_user_by_username(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        # Add other fields you want to return
    }
    return JsonResponse(user_data)

# Endpoint to retrieve user details by user ID
@csrf_exempt
def get_user_by_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        # Add other fields you want to return
    }
    return JsonResponse(user_data)
