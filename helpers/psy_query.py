import os, json
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from .prompts import SYS_PROMPT_1_psyq as SYS_PROMPT_1, SYS_PROMPT_2_psyq as SYS_PROMPT_2, SYS_PROMPT_3
from django.http import HttpResponse, JsonResponse
from .graph import get_graph_schema, get_graphConnection

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

def get_node_name_and_id(node):
    type = list(node.labels)[0]
    mapping = {
        'Accounts': 'Account_Name',
        'Contact' : 'Contact_Name',
        'Leads': 'Lead_Name',
        'Meetings': 'Title',
        'Tasks': 'Subject'
    }
    name = mapping.get(type)
    id = node.element_id
    return node.get(name), id
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
                    # print("relationship element: " ,element)
                    type = element.type
                    properties = {k: element[k] for k in element}
                    
                    startNode, startNode_id = get_node_name_and_id(element.nodes[0])
                    endNode, endNode_id = get_node_name_and_id(element.nodes[1])


                    # Add all this data in JSON format in relationships
                    relationship = {
                        # 'id': id,
                        'type': type,
                        'properties': properties,
                        'startNode': startNode,
                        'startNode_id': startNode_id,
                        'endNode': endNode,
                        'endNode_id': endNode_id
                    }
                    relationships.append(relationship)
                
                else:
                    
                    name, id = get_node_name_and_id(element)
                    properties = {k: element[k] for k in element}
                    # Add all this data in JSON format in nodes
                    node = {
                        'id': id,
                        'name': name,
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

@csrf_exempt
def query(question, graph_path):
        try:
            driver = get_graphConnection(graph_path)
            graph_schema = get_graph_schema(graph_path)

            result_1 = LLMlayer_1(SYS_PROMPT_1, question, graph_schema) #natural language, graph wise
            result_2 = LLMlayer_1(SYS_PROMPT_2, result_1, graph_schema) #query neo4j
            # result_3 = LLMlayer_1(SYS_PROMPT_3, result_2, graph_schema)

            if result_2.startswith("```") and result_2.endswith("```"):
                query_str = result_2.strip().replace("```", "").strip()
                if query_str.startswith("cypher"):
                    query_str = query_str.strip().replace("cypher", "").strip()
            else:
                query_str = result_2
            
            print("QUEYR: " ,query_str)
            if driver is None:
                print("Driver is not initialized!")
            else:
                records, summary, keys = driver.execute_query(query_str, database_="neo4j")
            driver.close()

            nodes, relationships = get_data(records, keys)
            print("NODES: " , nodes)
            print("Relationships: " ,relationships)
            cypher_response = f"""
            These are the nodes: {nodes}
            These are the relationships: {relationships}"""
            
            final_result = LLMlayer2(question, cypher_response) #query result  -> natural language
            response_data = {
            "message" : final_result,
            "nodes": [{"id": node["id"], "name": node["name"]} for node in nodes],
            "links": [{"source" : link["startNode_id"], "target": link["endNode_id"]} for link in relationships]
            }

            return HttpResponse(json.dumps(response_data, indent=4), content_type = 'application/json')

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
