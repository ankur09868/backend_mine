from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SentimentAnalysis, Conversation
import os
from openai import OpenAI
from topicmodelling.models import TopicModelling
from django.db.models import Avg
from django.http import JsonResponse
from .gpt_utils import prepare_gpt_prompt


def calculate_sentiment_score(trust, joy, sadness, anger):
    # Custom formula to calculate sentiment score
    return (0.5 * trust + 0.5 * joy) - (0.3 * sadness + 0.7 * anger)


def get_topic_data(contact_id):
    # Fetch topic data based on contact_id by joining with Conversation
    topic_modelling = TopicModelling.objects.filter(contact_id=contact_id).first()
    if topic_modelling:
        return topic_modelling.topics
    return []  # Return an empty list if no topics are found


def get_avg_sentiment_data(contact_id):
    sentiments = SentimentAnalysis.objects.filter(contact_id=contact_id)
    total_trust = total_joy = total_sadness = total_anger = 0
    count = sentiments.count()

    for sentiment in sentiments:
        total_trust += sentiment.trust_score
        total_joy += sentiment.joy_score
        total_sadness += sentiment.sadness_score
        total_anger += sentiment.anger_score

    avg_trust = total_trust / count if count else 0
    avg_joy = total_joy / count if count else 0
    avg_sadness = total_sadness / count if count else 0
    avg_anger = total_anger / count if count else 0

    return {
        'trust': avg_trust,
        'joy': avg_joy,
        'sadness': avg_sadness,
        'anger': avg_anger
    }


def generate_personalized_prompt(contact_id, channel):
    sentiment_data = get_avg_sentiment_data(contact_id)
    sentiment_score = calculate_sentiment_score(
        sentiment_data['trust'],
        sentiment_data['joy'],
        sentiment_data['sadness'],
        sentiment_data['anger']
    )

    # Fetch topic data for the contact
    topics = get_topic_data(contact_id)

    # Prepare GPT prompt based on sentiment score, channel, and topics
    gpt_prompt = prepare_gpt_prompt(sentiment_score, channel, topics)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates natural and engaging communication prompts."},
            {"role": "user", "content": gpt_prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


class GeneratePromptView(APIView):
    def post(self, request):
        contact_id = request.data.get('contact_id')
        channel = request.data.get('platform')

        if not contact_id or not channel:
            return Response(
                {"error": "Contact ID and channel are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prompt = generate_personalized_prompt(contact_id, channel)
            return Response({"prompt": prompt}, status=status.HTTP_200_OK)
        except SentimentAnalysis.DoesNotExist:
            return Response(
                {"error": "Sentiment data for the given contact ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except TopicModelling.DoesNotExist:
            return Response(
                {"error": "Topic data for the given contact ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
