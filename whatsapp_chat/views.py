from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests, json


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
                "type": "button"
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
def setFlow(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            flow = data.get('node_data')
            print(request.body)
            if flow is None:
                return HttpResponseBadRequest('Flow data is missing')

            # Assuming flow is already a dictionary, not a string
            nodes, adjList = convert_flow(flow)
            print("flow converted")
            print("adj list:", adjList)
            print("nodes:", nodes)
            
            target_url = 'http://localhost:3000/flowdata'  # Updated to match your endpoint
            response = requests.post(target_url, json={'adjacencyList': adjList, 'nodes': nodes})
            
            # Debugging information
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)
            
            if response.status_code == 200:
                return JsonResponse({'message': 'Flow converted and sent successfully'})
            else:
                return JsonResponse({'error': 'Failed to send the converted flow'}, status=500)

        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON data')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest('ONLY POST REQUEST ALLOWED')
