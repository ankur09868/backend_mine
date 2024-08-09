from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import os
from .vectorize import vectorize
from .table_from_img import data_from_image
from .upload_csv import upload_csv, upload_xls


@csrf_exempt
def dispatcher(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension == '.pdf':
            return vectorize(request)
            
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return data_from_image(request)
        elif file_extension == '.csv':
            return upload_csv(request)
        elif file_extension in ['.xls', '.xlsx']:
            return upload_xls(request)
        else:
            return HttpResponseBadRequest('Unsupported file type.')
    else:
        return HttpResponseBadRequest('No file uploaded.')
