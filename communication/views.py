from rest_framework import generics
from .models import SentimentAnalysis, BehavioralMetrics, Conversation, Message
from .insta_msg import group_messages_into_conversations
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from transformers import pipeline
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
import re
from simplecrm.models import CustomUser

from .serializers import (
    SentimentAnalysisSerializer,
    BehavioralMetricsSerializer,
    ConversationSerializer,
    MessageSerializer,
)

# Sentiment Analysis Views
class SentimentAnalysisListCreateView(generics.ListCreateAPIView):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

class SentimentAnalysisDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

# Behavioral Metrics Views
class BehavioralMetricsListCreateView(generics.ListCreateAPIView):
    queryset = BehavioralMetrics.objects.all()
    serializer_class = BehavioralMetricsSerializer

class BehavioralMetricsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BehavioralMetrics.objects.all()
    serializer_class = BehavioralMetricsSerializer

# Conversation Views
class ConversationListCreateView(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

# Message Views
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class GroupMessagesView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            group_messages_into_conversations()  # Call the function to group messages
            return Response({"message": "Messages grouped into conversations successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Initialize the sentiment analysis pipeline with truncation and padding
# classifier = pipeline(
#     "text-classification", 
#     model='bhadresh-savani/distilbert-base-uncased-emotion', 
#     top_k=None, 
#     truncation=True, 
#     max_length=512
# )

def clean_text(text):
    """Remove HTML tags and extra spaces from the text."""
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove extra spaces and normalize whitespace
    text = ' '.join(text.split())
    print(text)
    return text

def chunk_text(text, max_length=512):
    """Splits text into chunks of specified max_length (in tokens)."""
    tokens = text.split()  # Assuming space-separated tokens
    for i in range(0, len(tokens), max_length):
        yield ' '.join(tokens[i:i + max_length])

def analyze_sentiment(text):
    sentiment_scores = {'joy': 0, 'anger': 0, 'sadness': 0, 'fear': 0, 'love': 0, 'surprise': 0}
    # Clean the text before processing
    text = clean_text(text)
    chunks = list(chunk_text(text))

    # Analyze each chunk and aggregate scores
    for chunk in chunks:
        #results = classifier(chunk)
        #print("Classifier results:", results)  # Debugging line
        
        # Handle nested list structure
        if results and isinstance(results[0], list):
            results = results[0]  # Unpack the nested list
        
        for result in results:
            if isinstance(result, dict):  # Ensure result is a dictionary
                label = result.get('label', '').lower()
                if label in sentiment_scores:
                    sentiment_scores[label] += result.get('score', 0)
            else:
                print("Unexpected result format:", result)  # Debugging line
    
    # Average the scores by the number of chunks
    num_chunks = len(chunks)
    if num_chunks > 1:
        sentiment_scores = {k: v / num_chunks for k, v in sentiment_scores.items()}
    
    return sentiment_scores

@method_decorator(csrf_exempt, name='dispatch')
class SentimentAnalysisView(APIView):
    def post(self, request):
        try:
            conversation_id = request.data.get('conversation_id')
            
            if not conversation_id:
                return Response({'error': 'conversation_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the conversation and associated user
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            
            if not conversation.user:
                return Response({'error': 'Associated user not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            messages = conversation.messages
            user = conversation.user
            
            # Ensure the user exists in the database
            if not CustomUser.objects.filter(id=user.id).exists():
                return Response({'error': 'Associated CustomUser not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            # Run sentiment analysis
            sentiment_scores = analyze_sentiment(messages)
            
            # Save sentiment analysis results
            sentiment_analysis = SentimentAnalysis(
                user=user,
                message_id=conversation.id,
                joy_score=sentiment_scores.get('joy', 0),
                sadness_score=sentiment_scores.get('sadness', 0),
                anger_score=sentiment_scores.get('anger', 0),
                trust_score=sentiment_scores.get('love', 0),
                timestamp=timezone.now()
            )
            sentiment_analysis.save()
            
            return Response({'message': 'Sentiment analysis saved successfully.'}, status=status.HTTP_201_CREATED)
        
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except CustomUser.DoesNotExist:
            return Response({'error': 'Associated CustomUser not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Handle unexpected errors
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
