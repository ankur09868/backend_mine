from django.db import models
from django.db.models import Count
import re
from bs4 import BeautifulSoup
import quopri


def deduplicate_model(model_class: models.Model, unique_field: str):
    
    duplicates = model_class.objects.values(unique_field).annotate(count=Count('id')).filter(count__gt=1)

    for duplicate in duplicates:
        objs = model_class.objects.filter(**{unique_field: duplicate[unique_field]})
        objs_to_delete = objs[1:]
        for obj in objs_to_delete:
            obj.delete()

def clean_text(text):
    if not text:
        return ""

    # Step 1: Decode Quoted-Printable encoded text
    text = quopri.decodestring(text).decode('utf-8', errors='ignore')

    # Step 2: Remove MIME boundaries and headers
    text = re.sub(r'--\S+', '', text)
    text = re.sub(r'(Content-Type:.*|Content-Transfer-Encoding:.*|charset=.*)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Content-Type.*?texthtml', '', text, flags=re.IGNORECASE)

    # Step 3: Remove HTML tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()

    # Step 4: Remove URLs and unsubscribe links
    text = re.sub(r'https?:\/\/\S+|www\.\S+', '', text)

    # Step 5: Remove special characters
    text = re.sub(r'[^A-Za-z0-9\s\.,!?\'"-]', '', text)

    # Step 6: Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text
