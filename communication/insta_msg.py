from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, CustomUser, Message
from .serializers import MessageSerializer
import requests
from datetime import datetime

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
    # Get the email data from the request
    emails = request.data.get('emails', [])
    
    if not emails:
        return Response({"error": "No email data provided."}, status=status.HTTP_400_BAD_REQUEST)

    for email in emails:
        # Extract relevant fields from the email data
        sender = email.get('sender', 'unknown@example.com')  # Provide a default sender if needed
        content = email.get('content', '')
        sent_at = email.get('sent_at', datetime.now())
        platform='email'

        # Create message data for the serializer
        message_data = {
            'sender': 3,  # Adjust as necessary for your model
            'content': content,
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