import os, json
from dotenv import load_dotenv
from openai import OpenAI
from neo4j import GraphDatabase
from simplecrm.new_database import get_graphConnection
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = OPENAI_API_KEY)

def LLMlayer_1(SYS_PROMPT, USER_PROMPT, graph_schema):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": graph_schema},
            {"role": "user", "content": USER_PROMPT}
        ]
    )
    return response.choices[0].message.content

def LLMlayer_2(SYS_PROMPT, USER_PROMPT, graph_schema):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content" : graph_schema},
            {"role": "user", "content": USER_PROMPT}
        ]
    )
    return response.choices[0].message.content

def LLMlayer2(question, cypher_response):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who answers STRICTLY to what is asked, based on the info provided. DO NOT ADD DATA FROM THE INTERNET. YOU KNOW NOTHING ELSE EXCEPT THE DATA BEING PROVIDED TO YOU. Keep your answers concise and only the required information"},
            {"role": "user", "content": f"on asking a cypher query, this is the response recieved: {cypher_response} "},
            {"role": "assistant", "content": "Sure, please provide the data you would like converted into a paragraph."},
            {"role": "user", "content":f"""Based on the Nodes OR Relationships, craft a suitable response that also answers to the question: {question}."""}
        ]
    )
    return response.choices[0].message.content

def get_data(records, keys):
    nodes = []
    relationships = []

    for record in records:
        for key in keys:
            try:
                element = record[key]
                
                # Check if the element has a 'type' attribute, indicating it's a relationship
                if hasattr(element, 'type'):
                    # id = element.element_id
                    type = element.type
                    properties = {k: element[k] for k in element}
                    
                    # Try to get the start and end nodes, defaulting to empty strings if not found
                    startNode = element.nodes[0].get('name') or element.nodes[0].get('firstname') or element.nodes[0].get('productname', '')
                    endNode = element.nodes[1].get('name') or element.nodes[1].get('firstname') or element.nodes[1].get('productname', '')
                    
                    # Add all this data in JSON format in relationships
                    relationship = {
                        # 'id': id,
                        'type': type,
                        'properties': properties,
                        'startNode': startNode,
                        'endNode': endNode
                    }
                    relationships.append(relationship)
                
                else:
                    # id = record[key].element_id
                    # labels = list(element.labels)
                    properties = {k: element[k] for k in element}
                    
                    # Add all this data in JSON format in nodes
                    node = {
                        # 'id': id,
                        'properties': properties
                    }
                    nodes.append(node)
            
            except AttributeError as e:
                print(f"AttributeError: {e} - Occurred while processing key: {key}")
            except KeyError as e:
                print(f"KeyError: {e} - Occurred while accessing elements of record with key: {key}")
            except Exception as e:
                print(f"Exception: {e} - Occurred while processing record with key: {key}")

    return nodes, relationships

def get_graph_schema(graph):
    driver = get_graphConnection(graph)
    query = "MATCH(n) MATCH ()-[l]-() RETURN n,l"

    records,summary,keys = driver.execute_query(query, database_="neo4j")
    driver.close()
    nodes={}
    checkset= set()
    relationships=[]
    for record in records:
        for key in keys:
            element = record[key]
            if key =='n':
                label = list(element.labels)[0]
                properties = {k: element[k] for k in element}
                if label not in checkset:
                    checkset.add(label)
                    nodes[label] = properties
            else:
                internal_nodes = element.nodes
                start = list(internal_nodes[0].labels)[0]
                end = list(internal_nodes[1].labels)[0]
                type = element.type
                
                rel = f"(:{start})-[:{type}]->(:{end})"
                if rel not in checkset:
                    relationships.append(rel)
                    checkset.add(rel)
    return nodes, relationships
    

SYS_PROMPT_1 = """
You will be given a graph schema which tells about the nodes, their properties and possible relationships between them. Understand the schema.
You will also be given a question. based on what is being asked, reformulate the question for the graph.

Instructions: Return the reformed question only. Do not return anything else.

Examples-
#1 what product should be suggested to lead 8?
response:- Return all the products. Return characterestics of lead id 8. Also return if theres any relationship present.
"""

SYS_PROMPT_2 = f"""
Generate Cypher statement to query a graph database.
Instructions:
Do not use any other relationship types or properties that are not provided.

IF THE RELATIONSHIP DIRECTION IN THE GENERATED  CYPHER QUERY DOESNT MATCH TO ANY OF THE ALLOWED RELATIONSHIPS IN Schema. THEN REVERSE THE RELATIONSHIP

Note: Do not include any explanations or apologies in your responses.
Do not include two return statements.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Do not include node properties.

instead of [:r1|:r2|:r3] format, prefer use of [:r1|r2|r3] format

PROMOTE USE OF OPTIONAL MATCH
"""

@csrf_exempt
def query(request):
    if request.method == "POST":
        try:
            # Parse the incoming request
            data = json.loads(request.body)
            question = data.get("prompt")

            if not question:
                return HttpResponse(
                    "Error: Question is required",
                    status=400
                )

            # Define graph and execute functions
            graph_path = r"simplecrm/Neo4j-a71a08f7-Created-2024-07-25.txt"
            driver = get_graphConnection(graph_path)
            n_schema, r_schema = get_graph_schema(graph_path)
            graph_schema = f"""The nodes are: {n_schema}
The relationships are: {r_schema}"""

            result_1 = LLMlayer_1(SYS_PROMPT_1, question, graph_schema)
            result_2 = LLMlayer_2(SYS_PROMPT_2, result_1, graph_schema)

            if result_2.startswith("```") and result_2.endswith("```"):
                query_str = result_2.strip().replace("```", "").strip()
                if query_str.startswith("cypher"):
                    query_str = query_str.strip().replace("cypher", "").strip()
            else:
                query_str = result_2

            records, summary, keys = driver.execute_query(query_str, database_="neo4j")
            driver.close()

            nodes, relationships = get_data(records, keys)

            cypher_response = f"""
            These are the nodes: {nodes}
            These are the relationships: {relationships}"""

            final_result = LLMlayer2(question, cypher_response)
            
            return HttpResponse(
                f"Success: {final_result}",
                status=200
            )

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