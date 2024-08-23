from django.http import HttpResponse
from django.views import View
from interaction.models import Email
from django.utils import timezone
import logging
import uuid
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from urllib.parse import unquote

logger = logging.getLogger(__name__)
class TrackLinkView(View):
    def get(self, request, trackingId, linktrackingId, *args, **kwargs):
        # Get the original URL from the query parameters
        redirect_url = request.GET.get('redirect_url')
        
        if redirect_url:
            try:
                # Retrieve the email instance
                email_instance = Email.objects.get(tracking_id=trackingId)
                
                # Update the tracking information for the specific link
                link_found = False
                for link in email_instance.links:
                    if link['link_id'] == linktrackingId and not link['is_clicked']:
                        link['is_clicked'] = True
                        link['time_clicked'] = timezone.now().isoformat()
                        email_instance.save()
                        link_found = True
                        break
                
                if not link_found:
                    return HttpResponse("Link not found or already clicked", status=404)
                
                # Redirect the user to the original URL
                return HttpResponseRedirect(unquote(redirect_url))
            
            except Email.DoesNotExist:
                # Handle the case where the email with the given trackingId is not found
                return HttpResponse("Email not found", status=404)
        
        else:
            # Handle the case where no redirect URL is provided
            return HttpResponse("Invalid tracking link", status=400)

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