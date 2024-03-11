from accounts.models import Account
from django.contrib.auth.models import User

# Create a new user (if needed)
user = User.objects.create(username='dummy_user')

# Create dummy accounts
Account.objects.create(
    name='Dummy Account 1',
    email='dummy1@example.com',
    phone='1234567890',
    industry='SOFTWARE',
    website='https://www.example.com',
    description='This is a dummy account 1',
    createdBy=user
)

Account.objects.create(
    name='Dummy Account 2',
    email='dummy2@example.com',
    phone='9876543210',
    industry='HEALTHCARE',
    website='https://www.example.org',
    description='This is a dummy account 2',
    createdBy=user
)