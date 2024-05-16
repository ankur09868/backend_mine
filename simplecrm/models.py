from django.contrib.auth.models import AbstractUser
from django.db import models
from tenant.models import Tenant 
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
    organization = models.CharField(max_length=100)
    # Add role field to the user model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
