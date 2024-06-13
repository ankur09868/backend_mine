from django.http import HttpResponse
from django.views import View
from contacts import models as md  # Ensure this is the correct path to your Contact model
import logging

logger = logging.getLogger(__name__)

class TrackOpenView(View):
    def get(self, request, contact_id, *args, **kwargs):
      
        try:
            contact = md.Contact.objects.get(id=contact_id)
            contact.isActive = True
            contact.save()
            logger.debug(f"Contact {contact_id} activated.")
        except md.Contact.DoesNotExist:
            logger.error(f"Contact does not exist for ID: {contact_id}")
            return HttpResponse('Contact does not exist', status=404)

        # Return a 1x1 transparent pixel
        pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel_data, content_type='image/gif')

    @classmethod
    def get_count(cls):
        global count
        return count
