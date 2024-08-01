from .psy_query import query, get_graph_schema
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json, os
from openai import OpenAI
from storage.tables import get_tables_schema
from api.views import ExecuteQueryView
from django.urls import reverse
from django.test import Client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

graph_path = r"simplecrm/Neo4j-a71a08f7-Created-2024-07-25.txt"
graph_schema = get_graph_schema(graph=graph_path)

table_schema = get_tables_schema()

SYS_PROMPT = f"""
Given the Graph Schema : {graph_schema}
And the Table Schema : {table_schema}
Determine the question being asked would be most suitable answered by which document, table, graph or none of these.
Return your response in single word stating 'Graph', 'Table' or 'None'.
DO NOT INCLUDE ANY APOLOGIES OR SUGGESTIONS. JUST RETURN THE NAME OF THE CLASSIFIED CATEGORY.
"""

def classify(question):
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": f" Question: {question}"}
        ]
    )
    response = response.choices[0].message.content
    print(response)
    return response

@csrf_exempt
def dispatch(request):
    if request.method == "POST":
        try:
            # Parse the incoming request
            data = json.loads(request.body)
            question = data.get("prompt")
            print("rcvd question = " ,question)
            if not question:
                return HttpResponse(
                    "Error: Question is required",
                    status=400
                )
            
            type = classify(question)
            if type == "Table":
                view = ExecuteQueryView.as_view()
                response = view(request)
                result = response.data
                print("table result: " ,result)
            elif type == "Graph":
                result = query(request=request)
                print("graph result: " ,result)
            elif type == "None":
                print("None type is yet to be defined")
                result = "null"
            else:
                result = "Data doesnt belong with us"

            return HttpResponse( result ,status=200)
        except json.JSONDecodeError:
            return HttpResponse(
                "Error: Invalid JSON",
                status=400
            )
        except Exception as e:
            return HttpResponse(
                f"Error: {str(e)}",
                status=500
            )
    else:
        return HttpResponse(
            "Error: Only POST method is allowed",
            status=405
        )