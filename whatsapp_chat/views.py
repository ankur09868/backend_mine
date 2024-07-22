from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Conversation

@csrf_exempt
def save_conversations(request, contact_id):
    try:
        if request.method == 'POST':
            source = request.GET.get('source', '')
            body = json.loads(request.body)
            conversations = body.get('conversations', [])
            tenant = body.get('tenant')
            

            for message in conversations:
                text = message.get('text', '')
                sender = message.get('sender', '')

                # Create and save Conversation object
                Conversation.objects.create(contact_id=contact_id, message_text=text, sender=sender,tenant_id=tenant,source=source)

            print("Conversation data saved successfully!")
            return JsonResponse({"message": "Conversation data saved successfully!"}, status=200)

        return JsonResponse({"error": "Invalid request method"}, status=400)

    except Exception as e:
        print("Error while saving conversation data:", e)
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def view_conversation(request, contact_id):
    try:
        # Query conversations for a specific contact_id
        source = request.GET.get('source', '')
        conversations = Conversation.objects.filter(contact_id=contact_id,source=source).values('message_text', 'sender')

        # Format data as per your requirement
        formatted_conversations = []
        for conv in conversations:
            formatted_conversations.append({'text': conv['message_text'], 'sender': conv['sender']})

        return JsonResponse(formatted_conversations, safe=False)

    except Exception as e:
        print("Error while fetching conversation data:", e)
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def get_unique_instagram_contact_ids(request):
    try:
        unique_contact_ids = Conversation.objects.filter(source='instagram').values_list('contact_id', flat=True).distinct()
        return JsonResponse({"unique_contact_ids": list(unique_contact_ids)})
    except Exception as e:
        print("Error while fetching unique contact IDs:", e)
        return JsonResponse({"error": "Error while fetching unique contact IDs"}, status=500)