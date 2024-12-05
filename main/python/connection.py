import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Connection():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    @staticmethod
    def create_node_tx(tx, name, nodeType):
        create_node = ("""
            CREATE (n:{_nodeType})
            SET n.name = "{_name}"
            RETURN n.id AS node_id
        """).format(_nodeType = nodeType, _name = name)
        result = tx.run(create_node)
        return result.single()["node_id"]

    def create(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.create_node_tx, name, nodeType)
        return result
    
if __name__ == "__main__":
    load_dotenv()
    url = "neo4j://localhost:7687"
    user_ = "neo4j"
    password_ = os.environ.get("NEO4J_PASSWORD")
    con = Connection(url, user_, password_)

#   Testing connection and node creation
    con.create("Neza", "Character")