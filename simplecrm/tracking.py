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
            # Retrieve the email instance by its tracking ID
            email = Email.objects.get(tracking_id=tracking_id)

            # If the email is already open, update time spent first
            if email.is_open and email.last_open_time:
                email.update_time_spent(timezone.now())

            # Update the 'last_open_time' to the current time
            email.last_open_time = timezone.now()

            # Increment the 'open_count'
            email.open_count += 1

            # Mark the email as open
            email.is_open = True

            # Set the initial open time if not set
            if not email.time_open:
                email.time_open = timezone.now()

            # Save the changes
            email.save()

            logger.info(f"Email {tracking_id} marked as opened.")

        except Email.DoesNotExist:
            logger.error(f"Email does not exist for trackingId: {tracking_id}")
            return HttpResponse('Email does not exist', status=404)

        # Return a 1x1 transparent GIF pixel for tracking purposes
        pixel_data = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        return HttpResponse(pixel_data, content_type='image/gif')
