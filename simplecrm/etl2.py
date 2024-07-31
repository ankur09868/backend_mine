tables=[
    "hp_products",
    "hp_users"
]

table_mappings = {
    "hp_accounts" : "Accounts",
    "hp_calls" : "Call",
    "hp_contacts" : "Contact",
    "hp_interaction": "Interaction",
    "hp_leads": "Lead",
    "hp_meetings": "Meeting",
    "hp_products": "Product",
    "hp_reminder": "Reminder",
    "hp_tenant": "Tenant",
    "hp_tickets": "Ticket",
    "hp_vendors": "Vendor",
    "hp_psycho":"Lead",
    "hp_users":"User"
}

import os, json, psycopg2
from openai import OpenAI
from prompts import SYS_PROMPT_ETL
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
            dbname="postgres",
            user="nurenai",
            password="Biz1nurenWar*",
            host="nurenaistore.postgres.database.azure.com",
            port="5432"
        )

def fetch_table(table_name: str):
    try: 
        conn = get_db_connection()
        cur=conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(f"SELECT * FROM {table_name}")
            
            # Fetch all rows from the executed query
        data = cur.fetchall()
            
            # Close the cursor and connection
        cur.close()
        conn.close()


        def format_row(row) -> str:
            ans="{" + "\n"
            ans+=",".join(f' "{key}": "{value}"' for key, value in row.items())
            ans+="\n" + "}"
            return ans

        # Iterate through each row and format
        formatted_rows = [format_row(row) for row in data]

        return formatted_rows
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


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

# print(leads)

add_nodes(leads=leads)
add_connections()
