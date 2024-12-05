import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Connection():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    @staticmethod
    def merge_node_tx(tx, name, nodeType, attribute, value):
        merge_node = """
            MERGE (n:%(_nodeType)s {name: "%(_name)s"})
            SET n.%(_attribute)s = "%(_value)s"
            RETURN n.name AS name
        """ % {"_nodeType": nodeType, "_name": name, "_attribute": attribute, "_value": value}
        result = tx.run(merge_node)
        return result.single()["name"]
    
    @staticmethod
    def delete_node_tx(tx, name, nodeType):
        delete_node = """
            MATCH (n:%(_nodeType)s {name: "%(_name)s"})
            DELETE n
        """ % {"_nodeType": nodeType, "_name": name}
        result = tx.run(delete_node)
        return result

    def merge(self, name, nodeType, attributesDict):
        for attribute, value in attributesDict.items():
            with self._driver.session() as session:
                result = session.execute_write(self.merge_node_tx, name, nodeType, attribute, value)
        return result
    
    def delete(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.delete_node_tx, name, nodeType)
        return result
    
if __name__ == "__main__":
    load_dotenv()
    url = "neo4j://localhost:7687"
    user_ = os.environ.get("NEO4J_USER")
    password_ = os.environ.get("NEO4J_PASSWORD")
    con = Connection(url, user_, password_)

#   Testing connection and node merger
#    con.merge("Neza", "Character", {"birthYear": "10.000 A.C", "birthPlace": "Imperio Cobre Ardente"})

    con.delete("Neza", "Character")