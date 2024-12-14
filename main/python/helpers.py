class Node():
    def __init__(self, con):
        self.con = con
        self.name = "Name"
        self.label = "Label"
        self.properties = {}
        self.edges = []
        self.graph = {'nodes': [], 'edges': []}

    def setNode(self, name):
        if name == "":
            self.name = ''
            self.label = ''
            self.properties = {}
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

            self.graph = {'nodes': [], 'edges': []}
            graph = self.con.get_graph(name)
            for node in graph['nodes']:
                if node not in self.graph['nodes']:
                    self.graph['nodes'].append(node)
            
            for edge in graph['edges']:
                if edge not in self.graph['edges'] and {'source': edge['target'], 'target': edge['source'], 'type': edge['type']} not in self.graph['edges']:
                    self.graph['edges'].append(edge)


    def updateLabel(self, label):
        self.label = label 

    def updateNode(self, properties):
        self.properties = properties

    def addProperty(self):
        self.properties["Property"] = "Value"

    def addEdge(self):
        newEdge = Edge()
        self.edges.append(newEdge)

    def updateEdges(self, treatedEdges):
        self.edges = treatedEdges

    def mergeNode(self):
        self.con.rename(self.name, self.label, {'name': self.properties["name"]})
        self.name = self.properties["name"]
        self.con.merge(self.name, self.label, self.properties)
        print("node merged")

    def mergeEdge(self):
        for edge in self.edges:
            edgeData = edge.getData()
            self.con.merge_edge(self.name, self.label, edgeData)
    
    def deleteNode(self):
        self.con.delete(self.name, self.label)
        self.name = None

    def getData(self):
        # Changing the structure of properties to suit the jinja in index.html
        properties_list = []
        for property, value in self.properties.items():
            if property != "name":
                properties_list.append([property, value])

        edgesList = []
        for edge in self.edges:
            edgesList.append(edge.getData())

        return {
            "name": self.name,
            "label": self.label,
            "properties": properties_list,
            "edges": edgesList
        }

    def saveNode(self):
        print(self.getData())
        print("\n\n\nSaving Node\n\n\n")
        print("merging node")
        self.mergeNode()
        print("merging edges")
        self.mergeEdge()

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
    def __init__(self, properties = {"type": "Edge Type"}, name = "Name", label = "Label"):
        self.name = name
        self.label = label
        self.properties = properties
        
    def addProperty(self):
        self.properties["Property"] = "Value"

    def getData(self):
        properties_list = []
        for property, value in self.properties.items():
            properties_list.append([property, value])
        return {
            "name": self.name,
            "label": self.label,
            "properties": properties_list
        }