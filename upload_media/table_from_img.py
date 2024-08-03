from django.http import JsonResponse
import boto3, json, os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from storage.tables import upload_table, create_table
from django.views.decorators.csrf import csrf_exempt

def upload_image_to_s3(file, bucket, object_name=None, region="ap-south-1"):
    if object_name is None:
        object_name = file.name

    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.upload_fileobj(file, bucket, object_name)
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return object_name

def extract_table_from_image(doc_name):
    client = boto3.client('textract')
    response = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': 'nurenai',
                'Name': doc_name,
            }
        },
        FeatureTypes=['TABLES', 'FORMS']
    )
    data = json.dumps(response, indent=3)
    # print(data)
    textract_data = json.loads(data)
    return textract_data

def convert_into_df(textract_data):
    cells = [block for block in textract_data['Blocks'] if block['BlockType'] == 'CELL']
    
    table = {}
    for cell in cells:
        row = cell['RowIndex']
        col = cell['ColumnIndex']
        text = ''
        for relationship in cell.get('Relationships', []):
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    text_block = next(block for block in textract_data['Blocks'] if block['Id'] == child_id)
                    if text_block['BlockType'] == 'WORD':
                        text += text_block['Text'] + ' '
        
        text = text.strip()
        if row not in table:
            table[row] = {}
        table[row][col] = text

    table_list = []
    for row_index in sorted(table.keys()):
        row = []
        for col_index in sorted(table[row_index].keys()):
            row.append(table[row_index][col_index])
        table_list.append(row)

    # result = "\n".join(["!".join(row) for row in table_list])
    # data = StringIO(result)
    # df = pd.read_csv(data, sep="!")
    
    # print(df)
    return table_list

def delete_file(bucket, file, region= "ap-south-1"):
    try:
        s3_client = boto3.client('s3', region_name=region)
        s3_client.delete_object(Bucket=bucket, Key=file)
        print("Delete Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except ClientError as e:
        print(f"Error occurred: {e}")
        return False

@csrf_exempt
def table_from_image(request):
    try:
        if 'file' not in request.FILES:
            return JsonResponse({"status": 400, "message": "No file provided in the request"}, status=400)
        
        file = request.FILES['file']
        model_name = request.POST.get('model_name', None)
        table_name = request.POST.get('table_name', None)
        
        if table_name == None:
                table_name = os.path.splitext(file.name)[0]
        if (model_name and table_name) or (not model_name and not table_name):
            return JsonResponse({"status": 400, "message": f"""Either model_name or table_name must be provided, but not both.\nprovide model_name to upload table to database. \nprovide table_name to create a new table to database and upload data"""}, status=400)
        
        print("rcvd data with file and model name: " ,model_name)
        bucket = 'nurenai'
        file_name = 'upload.jpg'
        region = "ap-south-1"
        doc_name = upload_image_to_s3(file, bucket, file_name, region)
        if not doc_name:
            return JsonResponse({"status": 500, "message": "Failed to upload image to S3"}, status=500)
            
        textract_data = extract_table_from_image(doc_name)
        table_list = convert_into_df(textract_data)
        print("table list: " ,table_list)
        delete_file(bucket, file=file_name)

        if table_name:
            create_table(table_list, table_name)
        else:
            upload_table(table_list, model_name)

            

        return JsonResponse({"status": 200, "message": "File processed successfully"})
    
    except KeyError as e:
        return JsonResponse({"status": 400, "message": f"Key error: {e}"}, status=400)
    except NoCredentialsError:
        return JsonResponse({"status": 400, "message": "AWS credentials not available"}, status=400)
    except PartialCredentialsError:
        return JsonResponse({"status": 400, "message": "Incomplete AWS credentials provided"}, status=400)
    except boto3.exceptions.S3UploadFailedError:
        return JsonResponse({"status": 500, "message": "Failed to upload file to S3"}, status=500)
    except Exception as e:
        return JsonResponse({"status": 500, "message": f"Internal server error: {e}"}, status=500)
