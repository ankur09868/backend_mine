tables=[
    "accounts_account" ,
    "contacts_contact",
    "product_product",
    "vendors_vendor",
    "tenant_tenant",
    "simplecrm_customuser"

]

table_mappings = {
    "accounts_account" : "Accounts",
    "contacts_contact" : "Contact",
    "product_product": "Product",
    "vendors_vendor": "Vendor",
    "tenant_tenant": "Tenant",
    "simplecrm_customuser":"User"
}

import os, json
from openai import OpenAI
from helpers.prompts import SYS_PROMPT_ETL
from storage.tables import get_db_connection, fetch_table


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
    query += ",".join([f'{key}: "{value.strip()}"' for key, value in row.items()])
    query += "})"
    return query

def add_nodes(leads):
    query_list=[]

    for table in tables:
        table_data = fetch_table(table)
        
        for row in table_data:
            row = json.loads(row)
            query_list.append(create_node_query(row, table))
    for lead in leads:
        query_list.append(create_node_query(lead, table_name="hp_leads"))
        
    with open('nodes_list.json', 'w') as file:
        json.dump(query_list, file)
        print("json file exported!")    

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
    connections_data = fetch_table("hp_interactions")
    
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

conn = get_db_connection()
cursor = conn.cursor()
query =f"SELECT * from hp_wa"
cursor.execute(query)
results = cursor.fetchall()

leads=[]
for row in results:
    lead = get_leads(row)
    leads.append(lead)

add_nodes(leads=leads)
add_connections()
