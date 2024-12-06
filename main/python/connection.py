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
            MATCH (n:%(_nodeType)s {name: "%(_name)s"})-[e]-(n2)
            RETURN n, e.type AS edge, n2.name AS name_2
        """ % {"_nodeType": nodeType, "_name": name}
        result = tx.run(read_node)
        return result.data("n")[0]["n"]

    @staticmethod
    def search_node_tx(tx, search):
        search_node = """
            MATCH (n)
            WHERE n.name =~ '(?i).*%(_search)s.*'
            RETURN n.name AS name
        """ % {"_search": search}
        result = tx.run(search_node)
        return result.data()
    
    @staticmethod
    def merge_edge_tx(tx, name_1, nodeType_1, name_2, nodeType_2, property, value):
        merge_edge = """
            MERGE (n1:%(_nodeType_1)s {name: "%(_name_1)s"})
            MERGE (n2:%(_nodeType_2)s {name: "%(_name_2)s"})
            MERGE (n1)-[e:Edge]-(n2)
            SET e.%(_property)s = "%(_value)s"
            RETURN e
        """ % {"_nodeType_1": nodeType_1, "_name_1": name_1,
               "_nodeType_2": nodeType_2, "_name_2": name_2, "_property": property, "_value": value}
        result = tx.run(merge_edge)
        return result

#   Create and update a node and its properties, the node is chosen by name and nodeType
    def merge(self, name, nodeType, propertiesDict):
        for property, value in propertiesDict.items():
            with self._driver.session() as session:
                result = session.execute_write(self.merge_node_tx, name, nodeType, property, value)
        return result

#   Delete a node and its edges, the node is chosen by name and nodeType (barely used)
    def delete(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.delete_node_tx, name, nodeType)
        return result
    
#   Read the properties of a node, used to view the active node
    def read_node(self, name, nodeType):
        with self._driver.session() as session:
            data = session.execute_read(self.read_node_tx, name, nodeType)
        return data
    
#   Search a node based on name, used on the search bar to find a node to activate
    def search_node(self, search):
        with self._driver.session() as session:
            data = session.execute_read(self.search_node_tx, search)
        return data
    
#   Create and update an edge and its properties, the nodes can be created with no properties through this method
#   Use a property type instead of label to discriminate the edges, because it can be modified with this method
    def merge_edge(self, name_1, nodeType_1, name_2, nodeType_2, propertiesDict):
        for property, value in propertiesDict.items():
            with self._driver.session() as session:
                result = session.execute_write(
                    self.merge_edge_tx, name_1, nodeType_1, name_2, nodeType_2, property, value
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
#    con.merge("Gelboss", "Character", {"shard": "Autonomy", "summary": "One of the ten genesis shards"})

#   Testing deletion
#    con.delete("Neza", "Character")

#   Testing read
#    data = con.read_node("Neza", "Character")
#    print(data)

#   Testing search
#    data = con.search_node("e")
#    print(data)

#   Testing edge merger
#    con.merge_edge("Gelboss", "Character", "Neza", "Character", {"type": "Passion"})
#    con.merge_edge("Neza", "Character", "Death", "Character", {"type":"Herald", "summary" : "Neza proposed a bargain to become the Herald of Death in exchange for seeing her lost daughter"})