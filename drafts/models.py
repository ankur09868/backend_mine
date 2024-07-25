from django.db import models
from django.conf import settings
class drafts(models.Model):
    image_url = models.JSONField() 
    caption = models.TextField()
    access_token = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_story = models.BooleanField(default=False)
    is_reel = models.BooleanField(default=False)
    scheduled_date = models.DateField(null=True, blank=True)
    scheduled_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.caption
