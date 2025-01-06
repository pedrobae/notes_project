class Node():
    def __init__(self, con):
        self.con = con
        self.name = ""
        self.label = ""
        self.newName = None
        self.properties = []
        self.edges = []
        self.graph = {'nodes': [], 'edges': []}

    def setNode(self, name):
        if name == "":
            self.name = ''
            self.label = ''
            self.newName = None
            self.properties = []
            self.edges = []
            self.graph = {'nodes': [], 'edges': []}
        else:
            self.name = name
            
            node, label, _edges = self.con.read(name)
            self.label = label[0]

            self.properties = node
            
            self.edges = []
            for edge in _edges:
                self.edges.append(Edge(edge["properties"], edge["edgeNode"], edge["nodeLabel"][0]))

            self.graph = {'nodes': [{"name": self.name, 'label': self.label}], 'edges': []}
            graph = self.con.get_graph(name)
            for node in graph['nodes']:
                if node not in self.graph['nodes']:
                    self.graph['nodes'].append(node)
            
            for edge in graph['edges']:
                reversed = {
                    'source': edge['target'], 
                    'target': edge['source'], 
                    'type': edge['type']
                }
                if edge not in self.graph['edges'] and reversed not in self.graph['edges']:
                    self.graph['edges'].append(edge)


    def updateNode(self, label, name, properties, edges):
        self.newName = name
        self.label = label
        self.properties = properties
        self.edges = edges


    def mergeNode(self):
        self.con.rename(self.name, self.label, self.newName)
        self.name = self.newName
        print('Renamed')

        self.con.merge(self.name, self.label, self.properties)

    def mergeEdge(self):
        self.con.delete_edges(self.name, self.label)
        for edge in self.edges:
            edgeData = edge.getData()
            self.con.merge_edge(self.name, self.label, edgeData)
    
    def deleteNode(self):
        self.con.delete(self.name, self.label)
        self.name = None

    def getData(self):
        # Changing the structure of properties to suit the jinja in index.html
        edgesList = []
        for edge in self.edges:
            edgesList.append(edge.getData())

        return {
            "name": self.name,
            "label": self.label,
            "properties": self.properties,
            "edges": edgesList
        }

    def saveNode(self):
        print(self.getData())
        print("\n\n\nSaving Node\n\n")

        print("\nMerging node")
        self.mergeNode()
        
        print("\nMerging edges")
        self.mergeEdge()

        print('\n\nSaved\n\n')

    def expandGraph(self, name):
        expansion = self.con.get_graph(name)
        for node in expansion['nodes']:
            if node not in self.graph['nodes']:
                self.graph['nodes'].append(node)
        
        for edge in expansion['edges']:
            if edge not in self.graph['edges']:
                self.graph['edges'].append(edge)

    def setNodeExpand(self, name):
        self.name = name
            
        node, label, _edges = self.con.read(name)
        self.label = label[0]

        self.properties = node
            
        edges = []
        for edge in _edges:
            edges.append(Edge(edge["properties"], edge["edgeNode"], edge["nodeLabel"][0]))
            
        self.edges = edges

        self.expandGraph(name)

            
class Edge():
    def __init__(self, properties = [], name = "", label = "", type = ""):
        self.properties = properties
        self.name = name
        self.label = label
        self.type = type

    def getData(self):
        return {
            "type": self.type,
            "name": self.name,
            "label": self.label,
            "properties": self.properties
        }