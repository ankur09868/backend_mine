from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_whatsapp_tenant_table(request):
    query = '''
    CREATE TABLE IF NOT EXISTS whatsapp_tenant_data (
        business_phone_number_id VARCHAR(255) PRIMARY KEY,
        flow_data JSONB,
        adj_list JSONB,
        access_token VARCHAR(255),
        created_at TIMESTAMPTZ DEFAULT NOW()
    )
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(query)
    
    return JsonResponse({'message': 'Table created successfully'})
import json
@csrf_exempt
def insert_whatsapp_tenant_data(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        
        # Extract fields from the parsed data
        business_phone_number_id = data.get('business_phone_number_id')
        flow_data = data.get('flow_data')
        adj_list = data.get('adj_list')
        access_token = data.get('access_token')
        
        # Validate that all required fields are present
        if not business_phone_number_id or not flow_data or not adj_list or not access_token:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Insert or update data in the database
        query = '''
        INSERT INTO whatsapp_tenant_data (business_phone_number_id, flow_data, adj_list, access_token)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (business_phone_number_id) DO UPDATE
        SET flow_data = EXCLUDED.flow_data,
            adj_list = EXCLUDED.adj_list,
            access_token = EXCLUDED.access_token
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query, [business_phone_number_id, json.dumps(flow_data), json.dumps(adj_list), access_token])
        
        return JsonResponse({'message': 'Data inserted successfully'})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
def get_whatsapp_tenant_data(request):
    business_phone_number_id = request.GET.get('business_phone_id')
    
    if not business_phone_number_id:
        return JsonResponse({'error': 'business_phone_id query parameter is required'}, status=400)

    query = '''
    SELECT business_phone_number_id, flow_data, adj_list, access_token
    FROM whatsapp_tenant_data
    WHERE business_phone_number_id = %s
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(query, [business_phone_number_id])
        row = cursor.fetchone()
    
    if not row:
        return JsonResponse({'error': 'No data found for the given business_phone_number_id'}, status=404)
    
    data = {
        'business_phone_number_id': row[0],
        'flow_data': row[1],
        'adj_list': row[2],
        'access_token': row[3]
    }
    
    return JsonResponse(data)
