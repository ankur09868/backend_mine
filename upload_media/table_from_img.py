from django.http import JsonResponse
import boto3, json, threading, psycopg2, os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from simplecrm.get_column_name import get_model_fields, get_column_mappings

table_mappings = {
    "Lead": "leadss_lead",
    "Account": "accounts_account",
    "Contact": "contacts_contact",
    "Meeting": "meetings_meeting",
    "Call": "calls_calls",
}

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

def extract_table(doc_name):
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

def create_table(table_list, index):
    print("table_list: " ,table_list[0])
    conn = conn_cred
    cur = conn.cursor()
    table_name = "upload_%s" % index
    column_names = [str(x) for x in table_list[0]]
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        {', '.join(f'"{column}" VARCHAR(50)' for column in column_names)}
    );
    """
    cur.execute(create_table_query)
    conn.commit()
    for row in table_list[1:]:
        insert_data_query = f"""
        INSERT INTO {table_name} ({', '.join(f'"{column}" ' for column in column_names)})
        VALUES ({', '.join(['%s'] * len(column_names))});
        """
        cur.execute(insert_data_query, tuple(row))
        conn.commit()

    cur.execute(f"SELECT * FROM {table_name};")
    rows = cur.fetchall()
    print("\nData in the new PostgreSQL table:")
    for row in rows:
        print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()

conn_cred = psycopg2.connect(
        dbname="postgres",
        user="nurenai",
        password="Biz1nurenWar*",
        host="nurenaistore.postgres.database.azure.com",
        port="5432"
    )

def upload_to_table(data_list, model_name):
    columns = data_list[0]
    fields = get_model_fields(model_name)
    mappings = get_column_mappings(fields, columns)
    table_name = table_mappings.get(model_name)
    print(mappings)
    
    for index, item in enumerate(data_list[0]):
        if item in mappings.values():
            key_to_replace = next(key for key, value in mappings.items() if value == item)
            data_list[0][index] = key_to_replace
    print("table name: " ,table_name)
    column_names = [str(x) for x in data_list[0]]
    print("column list: " ,column_names)
    conn = conn_cred
    cur= conn.cursor()
    for row in data_list[1:]:
        insert_data_query = f"""
        INSERT INTO {table_name} ({', '.join(f'"{column}" ' for column in column_names)})
        VALUES ({', '.join(['%s'] * len(column_names))});
        """
        cur.execute(insert_data_query, tuple(row))
        print("testingg")
        conn.commit()
    cur.execute(f"SELECT * FROM {table_name};")
    rows = cur.fetchall()
    print("\nData in the PostgreSQL table:")
    for row in rows:
        print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()

index =0
index_lock = threading.Lock()

def table_from_image(request):
    global index
    try:
        if 'file' not in request.FILES:
            return JsonResponse({"status": 400, "message": "No file provided in the request"}, status=400)
        
        file = request.FILES['file']
        model_name = request.POST.get('model_name')
        bucket = 'nurenai'
        object_name = 'upload5.jpg'
        region = "ap-south-1"
        doc_name = upload_image_to_s3(file, bucket, object_name, region)
        if not doc_name:
            return JsonResponse({"status": 500, "message": "Failed to upload image to S3"}, status=500)
        
        textract_data = extract_table(doc_name)
        table_list = convert_into_df(textract_data)
        print(table_list)
        with index_lock:
            current_index= index
            index+=1

        # create_table(table_list, index)
        upload_to_table(table_list, model_name)

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


