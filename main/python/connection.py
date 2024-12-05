import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

class Connection():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    @staticmethod
    def merge_node_tx(tx, name, nodeType, property, value):
        merge_node = """
            MERGE (n:%(_nodeType)s {name: "%(_name)s"})
            SET n.%(_property)s = "%(_value)s"
            RETURN n.name AS name
        """ % {"_nodeType": nodeType, "_name": name, "_property": property, "_value": value}
        result = tx.run(merge_node)
        return result.single()["name"]
    
    @staticmethod
    def delete_node_tx(tx, name, nodeType):
        delete_node = """
            MATCH (n:%(_nodeType)s {name: "%(_name)s"})
            DETACH DELETE n
        """ % {"_nodeType": nodeType, "_name": name}
        result = tx.run(delete_node)
        return result
    
    @staticmethod
    def read_node_tx(tx, name, nodeType):
        read_node = """
            MATCH (n:%(_nodeType)s {name: "%(_name)s"})
            RETURN n
        """ % {"_nodeType": nodeType, "_name": name}
        result = tx.run(read_node)
        return result.data("n")[0]["n"]
    
    @staticmethod
    def merge_edge_tx(tx, name_1, nodeType_1, name_2, nodeType_2, edgeType, property, value):
        merge_edge = """
            MERGE (:%(_nodeType_1)s {name: "%(_name_1)s"}) -
            [e:%(_edgeType)s] ->
            (:%(_nodeType_2)s {name: "%(_name_2)s"})
            SET e.%(_property)s = "%(_value)s"
            RETURN e
        """ % {"_nodeType_1": nodeType_1, "_name_1": name_1, "_edgeType": edgeType,
               "_nodeType_2": nodeType_2, "_name_1": name_2, "_property": property, "_value": value}
        result = tx.run(merge_edge)
        return result

    def merge(self, name, nodeType, propertiesDict):
        for property, value in propertiesDict.items():
            with self._driver.session() as session:
                result = session.execute_write(self.merge_node_tx, name, nodeType, property, value)
        return result
    
    def delete(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.delete_node_tx, name, nodeType)
        return result
    
    def read_node(self, name, nodeType):
        with self._driver.session() as session:
            data = session.execute_read(self.read_node_tx, name, nodeType)
        return data
    
    def merge_edge(self, name_1, nodeType_1, name_2, nodeType_2, edgeType, propertiesDict):
        for property, value in propertiesDict.items():
            with self._driver.session() as session:
                result = session.execute_write(
                    self.merge_edge_tx, name_1, nodeType_1, name_2, nodeType_2, edgeType, property, value
                    )
        return result
    
if __name__ == "__main__":
    load_dotenv()
    url = "neo4j://localhost:7687"
    user_ = os.environ.get("NEO4J_USER")
    password_ = os.environ.get("NEO4J_PASSWORD")
    con = Connection(url, user_, password_)

#   Testing node merger
#    con.merge("Neza", "Character", {"birthYear": "10.000 B.C", "birthPlace": "Ardent Copper Empire"})

#   Testing deletion
#    con.delete("Neza", "Character")

#   Testing read
#    data = con.read_node("Neza", "Character")
#    print(data)