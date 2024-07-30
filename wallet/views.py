from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Transaction
from django.db import transaction
from decimal import Decimal, InvalidOperation  

@api_view(['POST'])
def recharge_wallet(request):
    user_id = request.data.get('user_id')
    amount = request.data.get('amount', 0)
    description = request.data.get('description', 'Recharge')

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    # Get or create the wallet for the user
    wallet, created = Wallet.objects.get_or_create(user_id=user_id)

    with transaction.atomic():
        # Update the balance
        wallet.balance += amount
        wallet.save()

        # Create a transaction record
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='Recharge',
            description=description
        )

    return JsonResponse({'balance': str(wallet.balance)}, status=200)

@api_view(['POST'])
def deduct_from_wallet(request):
    user_id = request.data.get('user_id')
    amount = request.data.get('amount', 0)
    description = request.data.get('description', 'Deduction')

    # Convert amount to Decimal
    try:
        amount = Decimal(amount)
    except (ValueError, InvalidOperation):
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    # Get the wallet for the user, creating it if it doesn't exist
    wallet, created = Wallet.objects.get_or_create(user_id=user_id)

    if wallet.balance < amount:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    with transaction.atomic():
        # Update the balance
        wallet.balance -= amount
        wallet.save()

        # Create a transaction record
        Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type='Deduction',
            description=description
        )

    return JsonResponse({'balance': str(wallet.balance)}, status=200)
    
@api_view(['GET'])
def get_last_n_transactions(request):
    user_id = request.GET.get('user_id')  # Get the user ID from the request
    n = request.GET.get('n', 1)  # Default to 5 if not specified

    # Ensure n is an integer
    try:
        n = int(n)
    except ValueError:
        return JsonResponse({'error': 'Invalid number of transactions'}, status=400)

    # Get the wallet for the user
    wallet = get_object_or_404(Wallet, user_id=user_id)  # Fetch the wallet using user_id

    # Fetch the last n transactions for the wallet
    transactions = Transaction.objects.filter(wallet=wallet).order_by('-id')[:n]

    # Prepare the response data
    transaction_list = [
        {
            'amount': str(transaction.amount),
            'transaction_type': transaction.transaction_type,
            'description': transaction.description,
            'timestamp': transaction.created_at.isoformat()  # Adjust according to your Transaction model
        }
        for transaction in transactions
    ]

    return JsonResponse({'transactions': transaction_list}, status=200)
@api_view(['GET'])
def get_wallet_balance(request):
    user_id = request.GET.get('user_id')
    wallet = get_object_or_404(Wallet, user_id=user_id)
    return JsonResponse({'balance': str(wallet.balance)}, status=200)

