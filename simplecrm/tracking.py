from django.http import HttpResponse
from django.views import View
from interaction.models import Email
from django.utils import timezone
import logging
import uuid

logger = logging.getLogger(__name__)
class TrackOpenView(View):
    def get(self, request, tracking_id, *args, **kwargs):
        try:
            email = Email.objects.get(tracking_id=tracking_id)
            email.is_open = True
            email.time_open = timezone.now()
            email.save()
            logger.debug(f"Tracking {tracking_id} marked as opened.")
        except Email.DoesNotExist:
            logger.error(f"Tracking does not exist for ID: {tracking_id}")
            return HttpResponse('Email does not exist', status=404)

        # Return a 1x1 transparent pixel
        pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel_data, content_type='image/gif')

    @classmethod
    def get_count(cls):
        global count
        return count