tables=[
    "accounts_2024_08_03" ,
    "contacts_2024_08_03",
    "leads_2024_08_03",
    "meetings_2024_08_03",
    "tasks_2024_08_03"

]

table_mappings = {
    "accounts_2024_08_03" : "Accounts",
    "contacts_2024_08_03" : "Contact",
    "leads_2024_08_03": "Leads",
    "meetings_2024_08_03": "Meetings",
    "tasks_2024_08_03": "Tasks"
}

import os, json
from openai import OpenAI
from helpers.prompts import SYS_PROMPT_ETL
from helpers.tables import fetch_table
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def get_leads(row):
    id = str(row[0])
    name = row[2]
    chat = row[3]
    stage = "Qualifying"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYS_PROMPT_ETL },
                {"role": "user", "content": chat }
            ]
        )
    answer = json.loads(response.choices[0].message.content)
    answer['name'] = name
    answer['id'] = id
    answer['stage'] = stage

    return answer

def create_node_query(row, table_name):
    
    query = f"CREATE (:{table_mappings[table_name]} {{"
    properties = []
    for key, value in row.items():
        # Replace spaces and special characters in keys
        clean_key = key.replace(' ', '_').replace('.', '_')
        # Escape double quotes in values
        clean_value = value.strip().replace('"', '\\"').replace('(Sample)', '')
        properties.append(f'{clean_key}: "{clean_value}"')

    # Join properties and close the query
    query += ", ".join(properties)
    query += "})"
    return query

@csrf_exempt
def add_nodes(request):
    query_list=[]

    for table in tables:
        table_data = fetch_table(table)
        
        for row in table_data:
            row = json.loads(row)
            query_list.append(create_node_query(row, table))
    # for lead in leads:
    #     query_list.append(create_node_query(lead, table_name="hp_leads"))
        
    with open('nodes_list.json', 'w') as file:
        json.dump(query_list, file)
        print("json file exported!")    
    return JsonResponse({ "message": "success."} , status =200)

def create_edge_query(row):
    # Check if all required keys are present
    required_keys = ['sourcenodetype', 'sourcenodeid', 'targetnodetype', 'targetnodeid', 'relationshiptype']
    if not all(key in row for key in required_keys):
        print(f"Missing keys in properties: {row}")
        return None
    row = json.loads(row)
    # Generate the Cypher query to create a relationship
    query = (
        f"MATCH (source:{row['sourcenodetype']} {{id: '{row['sourcenodeid']}'}}), "
        f"(target:{row['targetnodetype']} {{id: '{row['targetnodeid']}'}}) "
        f"CREATE (source)-[:{row['relationshiptype']}]->(target)"
    )
    
    return query

def add_connections():
    # Fetch connections data using fetch_table
    connections_data = fetch_table("")
    
    if not connections_data:
        print("No connections data found.")
        return

    # Generate Cypher queries for each connection
    query_list = []
    
    for row in connections_data:
        query_list.append(create_edge_query(row))
    
    with open('connections_list.json', 'w') as file:
        json.dump(query_list, file)
        print("json file exported!")

