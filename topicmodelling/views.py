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

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
   # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)  
    # Remove CSS media queries
    text = re.sub(r'@media[^{]*\{[^}]*\}', '', text)  
    # Remove date and time patterns
    text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}', '', text)
    # Remove numeric sequences and alphanumeric sequences
    text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
    text = re.sub(r'\b[A-Za-z0-9]{5,}\b', '', text)  # Remove alphanumeric sequences with 5 or more characters
    # Remove punctuation and unwanted characters
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]  # Remove stop words
    print(tokens)
    return ' '.join(tokens)

@csrf_exempt
@api_view(['POST'])
def perform_topic_modelling(request):
    try:
        # Fetch data from the Conversation table
        conversations = Conversation.objects.all().values('id', 'user_id', 'messages')
        if not conversations:
            return HttpResponse("No conversations available for topic modeling.")

        df = pd.DataFrame(conversations)

        # Preprocess the text data
        df['processed_message'] = df['messages'].apply(preprocess_text)

        # Check if there are any empty processed messages
        df = df[df['processed_message'].str.strip() != '']  # Remove rows with empty processed messages

        if df.empty:
            return HttpResponse("All conversations were filtered out after preprocessing.")

        # Vectorize text
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['processed_message'])

        # Apply LDA
        n_topics = min(11, len(df))  # Ensure at least as many topics as conversations, up to the number of documents
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(X)

        # Extract topics
        topics = []
        for index, topic in enumerate(lda.components_):
            top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
            topics.append(top_words)  # Top 10 words

        # Transform documents to topic space
        topic_distributions = lda.transform(X)

        # Assign the most probable topic to each conversation
        df['dominant_topic'] = topic_distributions.argmax(axis=1)

        # Save the results to TopicModelling table within a transaction
        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    # Check if the conversation exists in the Conversation table
                    conversation = Conversation.objects.get(id=row['id'])
                    
                    # Check if the conversation already has a topic modeling entry
                    if TopicModelling.objects.filter(conversation=conversation).exists():
                        print(f"Topic modeling entry already exists for conversation ID {row['id']}. Skipping.")
                        continue

                    topic_modelling = TopicModelling(
                        conversation=conversation,
                        user=conversation.user,  # Set user from Conversation
                        topics=topics[row['dominant_topic']] if row['dominant_topic'] < len(topics) else ["No topics generated"]
                    )
                    topic_modelling.save()

                except Conversation.DoesNotExist:
                    print(f"Conversation ID {row['id']} does not exist.")
                except IndexError:
                    print(f"IndexError for conversation ID {row['id']}: list index out of range.")

        return HttpResponse("Successfully performed topic modeling and saved to TopicModelling table.")

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
