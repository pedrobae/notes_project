from neo4j import GraphDatabase

class Connection():
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    @staticmethod
    def __merge_node_tx(tx, name, nodeType, property, value):
        merge_node = """MERGE (n:%(_nodeType)s {name: "%(_name)s"})
                        SET n.%(_property)s = "%(_value)s"
                        RETURN n.name AS name""" % {"_nodeType": nodeType, 
                                                    "_name": name, 
                                                    "_property": property, 
                                                    "_value": value}
        print('\nMerging node\n',merge_node)

        result = tx.run(merge_node)
        return result.single()["name"]
    
    @staticmethod
    def __rename_tx(tx, name, nodeType, newName):
        rename = """MERGE (n:%(_nodeType)s {name: "%(_name)s"})
                    SET n = {}
                    SET n.name = "%(_newName)s"
                    RETURN n.name AS name""" % {"_nodeType": nodeType, 
                                                "_name": name, 
                                                "_newName": newName}
        print('\nrenaming node\n', rename)

        result = tx.run(rename)
        return result.single()["name"]
    
    @staticmethod
    def __delete_node_tx(tx, name, nodeType):
        delete_node = """MATCH (n:%(_nodeType)s {name: "%(_name)s"})
                         DETACH DELETE n""" % {"_nodeType": nodeType, 
                                               "_name": name}
        result = tx.run(delete_node)
        return result
    
    @staticmethod
    def __delete_edges_tx(tx, name_1, nodeType_1):
        delete_edge = """MATCH (n1:%(_nodeType_1)s {name: "%(_name_1)s"})-[e:Edge]-(n)
                         DELETE e""" % {"_nodeType_1": nodeType_1, 
                                        "_name_1": name_1}
        print("\ndeleting edges\n", delete_edge)

        result = tx.run(delete_edge)
        return result
    
    @staticmethod
    def __read_tx(tx, name):
        edged = True
        read_node = """
            MATCH (n {name: "%(_name)s"})
            RETURN n as node, 
                   labels(n) as label
                   """ % {"_name": name}
        read_edges = """
            MATCH (n {name: "%(_name)s"})-[e]-(n2)
            RETURN n as node, 
                   labels(n) as label, 
                   properties(e) AS properties, 
                   n2.name AS edgeNode, 
                   labels(n2) AS nodeLabel
                   """ % {"_name": name}
        print("\nreading edges\n", read_edges)

        data = tx.run(read_edges).data()
        if data == []:
            edged = False
            print("reading node\n", read_node)
            data = tx.run(read_node).data()
        print('\nread data:\n', data)
        
        node = data[0]["node"]
        label = data[0]["label"]
        edge = []
        if edged:
            for dict in data:
                dict.pop("node")
                edge.append(dict)
        return node, label, edge
        

    @staticmethod
    def __search_node_tx(tx, search):
        search_node = """MATCH (n)
                         WHERE n.name =~ '(?i).*%(_search)s.*'
                         RETURN labels(n) AS label, n.name AS name""" % {"_search": search}
        print("\nsearching node\n", search_node)

        result = tx.run(search_node)
        return result.data()
    
    @staticmethod
    def __merge_edge_tx(tx, name_1, nodeType_1, name_2, nodeType_2, property, value):
        merge_edge = """MERGE (n1:%(_nodeType_1)s {name: "%(_name_1)s"})
                        MERGE (n2:%(_nodeType_2)s {name: "%(_name_2)s"})
                        MERGE (n1)-[e:Edge]-(n2)
                        SET e.%(_property)s = "%(_value)s"
                        RETURN e""" % {"_nodeType_1": nodeType_1, 
                                       "_name_1": name_1,
                                       "_nodeType_2": nodeType_2, 
                                       "_name_2": name_2, 
                                       "_property": property, 
                                       "_value": value}
        print("\nmerging edges\n", merge_edge)

        result = tx.run(merge_edge)
        return result
    
    @staticmethod
    def __rename_edge_tx(tx, name_1, nodeType_1, name_2, nodeType_2, edgeType):
        rename_edge = """MERGE (n1:%(_nodeType_1)s {name: "%(_name_1)s"})
                         MERGE (n2:%(_nodeType_2)s {name: "%(_name_2)s"})
                         MERGE (n1)-[e:Edge]-(n2)
                         SET e.type = '%(_edgeType)s'
                         RETURN e""" % {"_nodeType_1": nodeType_1, 
                                        "_name_1": name_1,
                                        "_nodeType_2": nodeType_2, 
                                        "_name_2": name_2, 
                                        "_edgeType": edgeType}
        print('\nrenaming edges\n', rename_edge)

        result = tx.run(rename_edge)
        return result
    
    @staticmethod
    def __get_graph_tx(tx, name):
        get_data = """MATCH (n1 {name: "%(_name)s"})-[e]-(n2)
                      RETURN n1, e, n2""" % {'_name': name}
        print('\ngetting data\n', get_data)

        result = tx.run(get_data)
        nodes = []
        edges = []
        for record in result:
            nodes.append({"name": record['n1']['name'], 'label': list(record['n1'].labels)})
            nodes.append({"name": record['n2']['name'], 'label': list(record['n2'].labels)})
            edges.append({'source': record['n1']['name'], 'target': record['n2']['name'], 'type': record['e']['type']})
        return {'nodes': nodes, 'edges': edges}

#   Create and update a node and its properties, the node is chosen by name and nodeType
    def merge(self, name, nodeType, propertiesList):
        for property in propertiesList:
            with self._driver.session() as session:
                session.execute_write(self.__merge_node_tx, name, nodeType, property[0], property[1])

            print("Merged")
    
#   Clears properties for renaming purposes
    def rename(self, name, nodeType, newName):
        with self._driver.session() as session:
            result = session.execute_write(self.__rename_tx, name, nodeType, newName)
        return result

#   Delete a node and its edges, the node is chosen by name and nodeType (barely used)
    def delete(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.__delete_node_tx, name, nodeType)
        return result
    
#   Read the properties of a node and its edges, used to view the active node
    def read(self, name):
        with self._driver.session() as session:
            data = session.execute_read(self.__read_tx, name)
        return data
    
#   Search a node based on name, used on the search bar to find a node to activate
    def search_node(self, search):
        with self._driver.session() as session:
            data = session.execute_read(self.__search_node_tx, search)
        return data
    
#   Create and update an edge and its properties, the nodes can be created with no properties through this method
#   Use a property type instead of label to discriminate the edges, because it can be modified with this method
    def merge_edge(self, name_1, nodeType_1, edgeData):
        with self._driver.session() as session:
                result = session.execute_write(self.__rename_edge_tx, 
                                               str(name_1), 
                                               nodeType_1, 
                                               edgeData["name"], 
                                               edgeData["label"],
                                               edgeData["type"])
        for property in edgeData["properties"]:
            with self._driver.session() as session:
                result = session.execute_write(self.__merge_edge_tx, 
                                               str(name_1), 
                                               nodeType_1, 
                                               edgeData["name"], 
                                               edgeData["label"], 
                                               property[0], 
                                               property[1])
        return result
    
#   Get node graph data based on name
    def get_graph(self, name):
        with self._driver.session() as session:
            data = session.execute_read(self.__get_graph_tx, name)
        return data
    
#   Delete the edges of a node
    def delete_edges(self, name, nodeType):
        with self._driver.session() as session:
            result = session.execute_write(self.__delete_edges_tx, 
                                           str(name), 
                                           nodeType)
            print('\nDeleted')
        return result