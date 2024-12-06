import os
from dotenv import load_dotenv

from connection import Connection

load_dotenv()
url = "neo4j://localhost:7687"
user_ = os.environ.get("NEO4J_USER")
password_ = os.environ.get("NEO4J_PASSWORD")

class Node():
    def __init__(self):
        self.con = Connection(url, user_, password_)
        self.name = None
        self.label = None
        self.properties = {}
        self.edges = {}

    def setNode(self, name, label):
        self.name = name
        self.label = label

    def setProperties(self, properties):
        self.properties = properties

    def updateDB(self):
        self.con.
