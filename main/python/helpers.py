class Node():
    def __init__(self, con):
        self.con = con
        self.name = "Name"
        self.label = "Label"
        self.properties = {}
        self.edges = []

    def setNode(self, name):
        if self.name != "Name":
            print("\n\n\nSaving Node\n\n\n")
            self.saveNode()

        self.name = name
        node, label, _edges = self.con.read(name)
        self.label = label[0]
        self.properties = node
        edges = []
        for edge in _edges:
            edges.append(Edge(edge["properties"], edge["edgeNode"], edge["nodeLabel"][0]))
        self.edges = edges

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
        self.con.merge(self.name, self.label, self.properties)
        self.name = self.properties["name"]

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
        self.mergeNode()
        self.mergeEdge()

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