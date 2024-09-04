
from django.apps import apps
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .utils import deduplicate_model
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from contacts.models import Contact
from .utils import clean_text
from django.db import connection, IntegrityError
import re


@api_view(['POST'])
def deduplicate_view(request):
    app_name = request.data.get('app-name')
    model_name = request.data.get('model')
    unique_field = request.data.get('field')
    
    if not app_name or not model_name or not unique_field :
        return JsonResponse({'status': 'error', 'message': 'app-name,model and field name are required.'}, status=400)
    
    try:
        model_class = apps.get_model(app_name, model_name)
    except LookupError:
        return JsonResponse({'status': 'error', 'message': f'Model {model_name} not found in App.'}, status=400)

    try:
        deduplicate_model(model_class, unique_field)
        return JsonResponse({'status': 'success', 'message': f'Duplicates removed successfully from {model_name}.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
# storing selected emails
@api_view(['POST'])
def store_selected_emails(request):
    selected_emails = request.data  # Expecting a list of emails

    with connection.cursor() as cursor:
        for email_data in selected_emails:
            email_id = email_data.get('email_id')
            from_address = email_data.get('from')
            subject = email_data.get('subject')
            text = email_data.get('text')

            # Clean the text to make it readable
            cleaned_text = clean_text(text)

            # Check if cleaned text field is empty or not provided
            if not cleaned_text:
                return Response(
                    {"error": f"Text field is missing or unreadable for email_id: {email_id}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Extract the email address from the "from" field
            email_match = re.search(r'<(.+?)>', from_address)
            extracted_email = email_match.group(1) if email_match else from_address.strip()

            # Find the contact_id based on the extracted email address
            contact_id = None
            try:
                contact = Contact.objects.get(email=extracted_email)
                contact_id = contact.id
            except Contact.DoesNotExist:
                return Response(
                    {"error": f"No contact found for email: {extracted_email}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Insert email into the selected_emails table with contact_id
            try:
                cursor.execute("""
                    INSERT INTO selected_emails (email_id, from_address, subject, text, contact_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (email_id) DO NOTHING;
                """, [email_id, from_address, subject, cleaned_text, contact_id])
            except IntegrityError as e:
                return Response(
                    {"error": f"Database integrity error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                return Response(
                    {"error": f"Unexpected error: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    return Response({"message": "Emails stored successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def fetch_all_emails(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT email_id, from_address, subject, text FROM selected_emails;")
        emails = cursor.fetchall()

    # Transform fetched data into a list of dictionaries
    email_list = [
        {
            "email_id": email[0],
            "from_address": email[1],
            "subject": email[2],
            "text": email[3],
        }
        for email in emails
    ]
    
    return Response(email_list, status=status.HTTP_200_OK)
