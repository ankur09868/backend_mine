from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests, json
from node_temps.models import Flow
from contacts.models import Contact
from django.db import connection


def convert_flow(flow):
    print("recieved flow: ", flow)
    node_blocks = flow['nodes']
    edges = flow['edges']

    nodes = []
    adjList = []
    id=0
    for node_block in node_blocks:
        if node_block['type'] == 'askQuestion':
            data = node_block['data']
            node = {
                "oldIndex": node_block["id"],
                "id": id,
                "body": data['question']
            }
            if data['optionType'] == 'Buttons':
                node["type"]="Button"
                nodes.append(node)
                list_id = id
                id+=1
                adjList.append([])
                for option in data['options']:
                    node ={
                        "id":id,
                        "body": option,
                        "type": "button_element"
                    }
                    nodes.append(node)
                    adjList.append([])
                    adjList[list_id].append(id)
                    id+=1
            elif data['optionType'] == 'Variables':
                node["type"]="Input"
                nodes.append(node)
                adjList.append([])
                id+=1

            elif data['optionType'] == 'Lists':
                node["type"]="List"
                nodes.append(node)
                list_id = id
                id+=1
                adjList.append([])
                for option in data['options']:
                    node ={
                        "id":id,
                        "body": option,
                        "type": "list_element"
                    }
                    nodes.append(node)
                    adjList.append([])
                    adjList[list_id].append(id)
                    id+=1

        elif node_block['type'] == 'sendMessage':
            data=node_block['data']
            node = {
                "oldIndex": node_block["id"],
                "id": id,
                "body": data['fields'][0]['content'],
                "type": "string"
            }
            nodes.append(node)
            adjList.append([])
            id+=1
        elif node_block['type'] == 'setCondition':
            data=node_block['data']
            node = {
                "oldIndex": node_block["id"],
                "id": id,
                "body": data['condition'],
                "type": "Button"
            }
            nodes.append(node)
            adjList.append([])
            list_id = id
            id+=1
            node = {
                "id": id,
                "body": "true",
                "type": "button_element"
            }
            nodes.append(node)
            adjList.append([])
            adjList[list_id].append(id)
            id+=1
            node = {
                "id": id,
                "body": "false",
                "type": "button_element"
            }
            nodes.append(node)
            adjList.append([])
            adjList[list_id].append(id)
            id+=1
            
    for edge in edges:
        source = int(edge['source'])
        target = int(edge['target'])
        suffix=0
        sourcehandle = edge['sourceHandle']
        if sourcehandle != None:
            if sourcehandle == "true":
                suffix+=1
            elif sourcehandle == "false":
                suffix+=2
            else:
                suffix+=int(sourcehandle[-1]) + 1
        for node in nodes:
            if 'oldIndex' in node:  # Check if 'oldIndex' exists in the node
                if int(node['oldIndex']) == source:
                    n_source = int(node['id'])+suffix
                if int(node['oldIndex']) == target:
                    n_target = int(node['id'])
                    
        adjList[n_source].append(n_target)  # Use source as an integer index
    
    for node in nodes:
        node.pop('oldIndex', None)
    return nodes, adjList

@csrf_exempt
def saveFlow(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            flow_data = data.get('node_data')
            phone_number = data.get('phoneNumber', '917906511071')
            print("Request body:", request.body)

            if flow_data is None:
                return HttpResponseBadRequest('Flow data is missing')

            # Optional: Uncomment this block to fetch the contact directly via Django ORM
            # try:
            #     contact = Contact.objects.get(phone=phone_number)
            #     print("CONTACTS: ", contact)
            # except Contact.DoesNotExist:
            #     error_message = f"No contact found with phone number: {phone_number}"
            #     print("Error:", error_message)
            #     return JsonResponse({'error': error_message}, status=404)

            # Convert the flow data into nodes and adjacency list
            nodes, adjList = convert_flow(flow_data)
            currNode = 0
            ai_mode = False
            print("Flow converted")
            print("Adjacency list:", adjList)
            print("Nodes:", nodes)

            nodes_json = json.dumps(nodes)
            adjList_json = json.dumps(adjList)

            # Fetch the contact ID from the database using the phone number
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id FROM contacts_contact WHERE phone = %s;
                """, (phone_number,))
                contact_row = cursor.fetchone()

            if contact_row:
                contact_id = contact_row[0]
                print("Contact ID found:", contact_id)
                insert_query = """
                    INSERT INTO node_temps_flow (nodes, adj_list, contact_id, curr_node, ai_mode)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                """
                with connection.cursor() as cursor:
                    cursor.execute(insert_query, (nodes_json, adjList_json, contact_id, currNode, ai_mode))
                    flow_id = cursor.fetchone()[0]
                    print("Data inserted successfully with Flow ID:", flow_id)
                    connection.commit()
            else:
                print("No contact found")
                return JsonResponse({'error': 'No contact found for the provided phone number'}, status=404)

            print("Flow saved successfully")
            return JsonResponse({'message': "Flow saved successfully"})

        except json.JSONDecodeError as json_err:
            print("JSONDecodeError:", json_err)
            return HttpResponseBadRequest('Invalid JSON data')
        except Exception as e:
            print("Exception:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
    else:
        print("Invalid request method:", request.method)
        return HttpResponseBadRequest('ONLY POST REQUEST ALLOWED')


@csrf_exempt
def get_flow(request):
    try:
        print("getflow")
        data = json.loads(request.body)
        phoneNumber = str(data.get('phone_number'))

        if not phoneNumber:
            return JsonResponse({'error': 'phone_number is required'}, status=400)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT ntf.nodes, ntf.adj_list, ntf.curr_node, ntf.ai_mode
                FROM node_temps_flow ntf
                INNER JOIN contacts_contact c ON ntf.contact_id = c.id
                WHERE c.phone = %s;
            """, (phoneNumber,))
            row = cursor.fetchone()

        if row:
            nodes, adj_list, curr_node, ai_mode = row
            return JsonResponse({
                'nodes': nodes,
                'adj_list': adj_list,
                'curr_node': curr_node,
                'ai_mode': ai_mode
            })
        else:
            return JsonResponse({'error': 'No data found for the given phone number'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    finally:
        if connection:
            connection.close()
    
@csrf_exempt
def set_flow(request):
    try:
        data = json.loads(request.body)
        phoneNumber = str(data.get('phone_number'))
        curr_node = data.get('curr_node')
        ai_mode = data.get('ai_mode')

        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT id FROM contacts_contact WHERE phone = %s;
        """, (phoneNumber,))
        contact_row = cursor.fetchone()

        if contact_row:
            contact_id = contact_row[0]
            print("Contact ID found:", contact_id)

            update_query = """
                UPDATE node_temps_flow
                SET curr_node = %s, ai_mode = %s
                WHERE contact_id = %s
            """
            cursor.execute(update_query, (curr_node, ai_mode, contact_id))
            
            connection.commit()
            print("data updated")
            return JsonResponse({"message": "Data updated successfully"})

        else:
            return JsonResponse({"error": "No contact found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    finally:
        if connection:
            connection.close()


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

@csrf_exempt
def update_message_status(request):
    business_phone_number_id = request.POST.get('business_phone_number_id')
    isRead = request.POST.get('is_read')
    isDelivered = request.POST.get('is_delivered')
    isSent = request.POST.get('is_sent')
    phone_number = request.POST.get('user_phone')
    messageID = request.POST.get('message_id')

    query = f"""
INSERT INTO whatsapp_message_id (message_id ,business_phone_number_id, sent, delivered, read, user_phone_number)
VALUES ({messageID},{business_phone_number_id}, {isSent}, {isDelivered}, {isRead}, {phone_number})
ON CONFLICT (message_id)
DO UPDATE SET
    business_phone_number_id = EXCLUDED.business_phone_number_id
    sent = EXCLUDED.sent,
    delivered = EXCLUDED.delivered,
    read = EXCLUDED.read,
    user_phone_number = EXCLUDED.user_phone_number; 

"""
    with connection.cursor() as cursor:
        cursor.execute(query)
    
    
    return JsonResponse({'message': 'Data inserted successfully'})

@csrf_exempt
def get_status(request):
    if request.method == 'GET':
        query = """
            SELECT *
            FROM whatsapp_message_id;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            message_statuses = [
                {
                    "business_phone_number_id": row[0],
                    "is_sent": row[1],
                    "is_delivered": row[2],
                    "is_read": row[3],
                    "user_phone_number": row[4],
                    "message_id": row[5],
                }
                for row in rows
            ]

            return JsonResponse({"message_statuses": message_statuses})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
