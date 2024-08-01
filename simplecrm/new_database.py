from dotenv import load_dotenv
import os, json
from neo4j import GraphDatabase
from storage.graph import get_graphConnection

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
