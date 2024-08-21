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

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
   # Remove other unwanted characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()  # Convert to lowercase
    # Remove HTML and CSS tags
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'@media[^{]*\{[^}]*\}', '', text)  # Remove CSS media queries
    # Remove date and time patterns (e.g., 2024-08-07 06:36:58.672213+00:00)
    text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}', '', text)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = word_tokenize(text)  # Tokenize
    tokens = [word for word in tokens if word not in stop_words]  # Remove stop words
    print(tokens)
    return ' '.join(tokens)

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
        if df['processed_message'].str.strip().eq('').any():
            return HttpResponse("One or more conversations have no valid text after preprocessing.")

        # Vectorize text
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['processed_message'])

        # Apply LDA
        lda = LatentDirichletAllocation(n_components=9, random_state=42)
        lda.fit(X)

        # Extract topics
        topics = []
        for index, topic in enumerate(lda.components_):
            top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
            topics.append(top_words)  # Top 10 words

        # Debugging output
        if len(topics) < df.shape[0]:
            return HttpResponse(f"Number of topics generated ({len(topics)}) is less than the number of conversations ({df.shape[0]}).")

        # Save the results to TopicModelling table within a transaction
        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    # Check if the conversation exists in the Conversation table
                    conversation = Conversation.objects.get(id=row['id'])
                    
                    # Check if the conversation already has a topic modeling entry
                    if not TopicModelling.objects.filter(conversation=conversation).exists():
                        topic_modelling = TopicModelling(
                            conversation=conversation,
                            user=conversation.user,  # Set user from Conversation
                            topics=topics[idx] if idx < len(topics) else ["No topics generated"]
                        )
                        topic_modelling.save()
                    else:
                        return HttpResponse(f"Topic modeling entry already exists for conversation ID {row['id']}.")

                except Conversation.DoesNotExist:
                    return HttpResponse(f"Conversation ID {row['id']} does not exist.")
                except IndexError:
                    return HttpResponse(f"IndexError for conversation ID {row['id']}: list index out of range.")

        return HttpResponse("Successfully performed topic modeling and saved to TopicModelling table.")

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
