from dotenv import load_dotenv
import os, json
from neo4j import GraphDatabase

def get_graphConnection(graph):
        
    load_status = load_dotenv(graph)
    if not load_status:
        print("Failed to load environment variables. Please check the .env file and its path.")

    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")

    return GraphDatabase.driver(URI, auth = (USERNAME, PASSWORD))

def create(graph_entities, entity):
    driver = get_graphConnection()
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for command in graph_entities:
                tx.run(command)
                print(f"{entity} created succesfully!")

if __name__ == "__main__":
    with open('nodes_list.json', 'r') as file:
        nodes = json.load(file)

    create(nodes, "node")
    # print("NODES RCVD: " ,nodes)
    with open('connections_list.json', 'r') as file:
        edges = json.load(file)
    create(edges, "edge")
