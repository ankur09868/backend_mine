from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests

def convert_flow(flow):
    adjList=""
    nodes=[]
    return adjList, nodes

@csrf_exempt
def setFlow(request):
    if request.method == 'POST':
        flow = request.POST.get('flow')

        if flow is None:
            return HttpResponseBadRequest('Flow data is missing')

        adjList, nodes = convert_flow(flow)


        target_url = 'http://localhost:3000/flow-data'
        response = requests.post(target_url, json = {'adjacencyList': adjList, 'nodes': nodes})

        if response.status_code == 200:
            return JsonResponse({'message': 'Flow converted and sent successfully'})
        else:
            return JsonResponse({'error': 'Failed to send the converted flow'}, status=500)

    else:
        return HttpResponseBadRequest('ONLY POST REQUEST ALLOWED')
