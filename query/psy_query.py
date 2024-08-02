import os, json
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from helpers.prompts import SYS_PROMPT_1_psyq as SYS_PROMPT_1, SYS_PROMPT_2_psyq as SYS_PROMPT_2
from django.http import HttpResponse
from storage.graph import get_graph_schema, get_graphConnection

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

@csrf_exempt
def query(question, graph_path):
        try:
            driver = get_graphConnection(graph_path)
            graph_schema = get_graph_schema(graph_path)

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
