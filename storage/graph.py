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
