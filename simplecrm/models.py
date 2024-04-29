from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Define choices for user roles
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
    MANAGER = 'manager'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee'),
        (MANAGER, 'Manager'),
    ]

    # Add role field to the user model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)
