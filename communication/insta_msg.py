from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, CustomUser, Message
from .serializers import MessageSerializer
import requests
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from simplecrm.utils import clean_text
from django.core.exceptions import ObjectDoesNotExist
from contacts.models import Contact
from .utils import extract_email

@api_view(['POST'])
def save_messages(request):


    url = "https://graph.facebook.com/v20.0/aWdfZAG06MTpJR01lc3NhZA2VUaHJlYWQ6MTc4NDE0NjY0MDkwMzM0ODk6MzQwMjgyMzY2ODQxNzEwMzAxMjQ0Mjc2MDIwNDc4NzU3MzAwNjEx/messages?fields=message&access_token=EAAVZBobCt7AcBOxjceit3l5VYrgU6QTGzzi34BZBsRM85EXW8fXvfg4KEZCEFfz62u6TjRxpGozYFQjkZBXvZCplbyeqySwW685UKYK0tlGuL8FyLYa6NgnyGH2mA7nI3upp5dGwQyiTvawPWQ9cf9eTWp9Rvv5nZCAgko5wxWovIoU5UJZCozGW3ZBTusgk6AHOC8mtLlCa0AsLQlmiA8GJtlve"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()

        for item in data['data']:
        # Skip empty messages if needed
            if item['message']:
                message_data = {
                    'sender': 3,
                    'content': item['message'],
                    'sent_at': datetime.now()
                }

                serializer = MessageSerializer(data=message_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Messages saved successfully."}, status=status.HTTP_201_CREATED)

    except requests.exceptions.HTTPError as http_err:
        return Response({"error": f"HTTP error occurred: {http_err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        return Response({"error": f"Other error occurred: {err}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_email_messages(request):
    #   # Debug: print the incoming request data
    # print("Incoming request data:", request.data)
    
    # Get the email data from the request
    emails = request.data.get('emails', [])
    
    if not emails:
        return Response({"error": "No email data provided."}, status=status.HTTP_400_BAD_REQUEST)

    for email in emails:
        # Extract relevant fields from the email data
        sender = email.get('sender', 'unknown@example.com')  # Provide a default sender if needed
        content = email.get('content', '')
        sent_at = email.get('sent_at')
        if not sent_at:
            sent_at = timezone.now().isoformat()
        platform='email'

         # Clean the content
        cleaned_content = clean_text(content)

        # Create message data for the serializer
        message_data = {
            'sender': 3,  # Adjust as necessary for your model
            'content': cleaned_content,
            'sent_at': sent_at,
            'platform':platform,
            'userid':sender
        }

        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Emails saved successfully."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def fetch_all_email_ids(request):
    # Retrieve unique email IDs
    email_ids = Message.objects.filter(platform='email').values_list('id', flat=True).distinct()

    # Prepare the response data as a list of unique email IDs
    email_id_list = list(email_ids)

    return Response(email_id_list, status=status.HTTP_200_OK)

def group_messages_into_conversations():
    # Fetch only messages that haven't been mapped, ordered by sent_at
    messages = Message.objects.filter(mapped=False).order_by('sent_at')

    # Group messages by user and platform
    grouped_messages = {}
    for message in messages:
        key = (message.userid, message.platform)
        if key not in grouped_messages:
            grouped_messages[key] = []
        grouped_messages[key].append(message)

    # Now process the grouped messages to create conversations
    for (userid, platform), message_group in grouped_messages.items():
        current_conversation = []

        # Sort the messages by sent_at
        message_group.sort(key=lambda x: x.sent_at)

        for message in message_group:
            if not current_conversation:
                current_conversation.append(message)
            else:
                last_message_time = current_conversation[-1].sent_at
                # Set a time threshold (e.g., 30 minutes)
                if message.sent_at - last_message_time <= timedelta(minutes=30):
                    current_conversation.append(message)
                else:
                    # Save the current conversation to the database
                    save_conversation(current_conversation, userid, platform)
                    current_conversation = [message]

        if current_conversation:
            save_conversation(current_conversation, userid, platform)

        # After saving conversations, mark these messages as mapped
        for msg in current_conversation:
            msg.mapped = True
            msg.save() 

def save_conversation(message_group, userid, platform):
    contact_id = None
    try:
         # Extract email if userid contains angle brackets
        email = extract_email(userid)
        
        # Try to find the contact by email first
        contacts = Contact.objects.filter(email=email)
        if contacts.exists():
            contact_id = contacts.first().id
        else:
            # If not found by email, try to find by phone number
            contacts = Contact.objects.filter(phone=userid)
            if contacts.exists():
                contact_id = contacts.first().id
            else:
                print("not added")
                return 
    
    except ObjectDoesNotExist:
        return

    # Combine messages into a single string
    combined_messages = "\n".join([f"{message.sent_at}: {message.content}" for message in message_group])

    # Create a unique conversation_id (you can adjust this logic as needed)
    conversation_id = f"{userid}_{platform}_{timezone.now().timestamp()}"

    # Create a new Conversation object
    Conversation.objects.create(
        user=message_group[0].sender,  # Set the user (or change as necessary)
        conversation_id=conversation_id,
        messages=combined_messages,  # Store the combined messages
        platform=platform,
        contact_id_id=contact_id  # Set the contact_id
    )