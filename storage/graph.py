from dotenv import load_dotenv
import os
from neo4j import GraphDatabase


def get_graphConnection(graph):
        
    load_status = load_dotenv(graph)
    if not load_status:
        print("Failed to load environment variables. Please check the .env file and its path.")

    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    return GraphDatabase.driver(URI, auth = (USERNAME, PASSWORD))


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
    graph_schema = f"""The nodes are: {nodes}
    The relationships are: {relationships}"""
    return graph_schema

