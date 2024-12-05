import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Connection():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    @staticmethod
    def merge_node_tx(tx, name, nodeType):
        merge_node = """
            MERGE (n:%(_nodeType)s {name: "%(_name)s"})
            RETURN n.name AS name
        """ % {"_nodeType": nodeType, "_name": name}
        result = tx.run(merge_node)
        return result.single()["name"]

    def create(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.merge_node_tx, name, nodeType)
        return result
    
if __name__ == "__main__":
    load_dotenv()
    url = "neo4j://localhost:7687"
    user_ = os.environ.get("NEO4J_USER")
    password_ = os.environ.get("NEO4J_PASSWORD")
    con = Connection(url, user_, password_)

#   Testing connection and node creation
    con.create("Neza", "Character")