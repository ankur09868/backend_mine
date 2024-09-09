# Importing necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from django.shortcuts import HttpResponse
from topicmodelling.models import TopicModelling, Conversation 
from simplecrm.models import CustomUser
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from contacts.models import Contact

# Downloading stopwords and punkt tokenizer
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Preprocessing the text by removing unwanted patterns and stop words
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'@media[^{]*\{[^}]*\}', '', text)
    text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}', '', text)
    text = re.sub(r'\b\w{2,}_\w{32}\b', '', text)  
    text = re.sub(r'\b\d+\b', '', text)
    text = re.sub(r'\b[A-Za-z0-9]{5,}\b', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

@csrf_exempt
@api_view(['POST'])
def perform_topic_modelling(request):
    try:
        # Extracting conversation IDs from the request
        conversation_ids = request.data.get('conversation_ids', [])
        if not conversation_ids:
            return Response({"error": "No conversation IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetching the conversations using provided IDs
        conversations = Conversation.objects.filter(id__in=conversation_ids).values('id', 'user_id', 'messages', 'contact_id')
        if not conversations:
            return Response({"error": "No conversations found for the provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        df = pd.DataFrame(conversations)

        # Preprocess the text data
        df['processed_message'] = df['messages'].apply(preprocess_text)
        df = df[df['processed_message'].str.strip() != '']  # Removing rows with empty processed messages

        if df.empty:
            return Response({"message": "All conversations were filtered out after preprocessing."}, status=status.HTTP_200_OK)

        # Count the number of words in each processed message
        df['word_count'] = df['processed_message'].apply(lambda x: len(x.split()))

        # Determine the number of topics based on word count
        df['n_topics'] = df['word_count'].apply(lambda count: 5 if count > 20 else min(3, len(df)))

        # Vectorizing the text data
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['processed_message'])

        # Applying LDA for each conversation based on its word count
        topics_list = []
        for _, row in df.iterrows():
            n_topics = row['n_topics']
            lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
            lda.fit(X)

            # Extracting topics with dynamic top words based on word count
            topics = []
            top_word_count = 2 if row['word_count'] < 10 else 5  # Adjust top words count
            for topic in lda.components_:
                top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-top_word_count:]]  # Adjust top words count dynamically
                topics.append(top_words)
                

            topics_list.append(topics)

        df['topics'] = topics_list

        # Assign the most probable topic to each conversation
        topic_distributions = lda.transform(X)
        df['dominant_topic'] = topic_distributions.argmax(axis=1)

        # Save the results to the TopicModelling table within a transaction
        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    # Check if the conversation exists in the Conversation table
                    conversation = Conversation.objects.get(id=row['id'])

                    # Fetch the associated Contact object
                    contact = Contact.objects.get(id=row['contact_id'])

                    # Check if the conversation already has a topic modeling entry
                    if TopicModelling.objects.filter(conversation=conversation).exists():
                        print(f"Topic modeling entry already exists for conversation ID {row['id']}. Skipping.")
                        continue

                    topic_modelling = TopicModelling(
                        conversation=conversation,
                        user=CustomUser.objects.get(id=row['user_id']),  # Set user from Conversation
                        topics=row['topics'][row['dominant_topic']] if row['dominant_topic'] < len(row['topics']) else ["No topics generated"],
                        contact_id=contact  # Assign the contact
                    )
                    print(topics)
                    topic_modelling.save()

                except Conversation.DoesNotExist:
                    print(f"Conversation ID {row['id']} does not exist.")
                except Contact.DoesNotExist:
                    print(f"Contact ID {row['contact_id']} does not exist for conversation ID {row['id']}.")
                except IndexError:
                    print(f"IndexError for conversation ID {row['id']}: list index out of range.")

        return Response({"message": "Successfully performed topic modeling and saved to TopicModelling table."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
