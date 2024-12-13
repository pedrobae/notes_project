class Node():
    def __init__(self, con):
        self.con = con
        self.name = "Name"
        self.label = "Label"
        self.properties = {}
        self.edges = []

    def setNode(self, name):
        self.name = name
        node, label, _edges = self.con.read(name)
        self.label = label[0]
        self.properties = node
        print("\n", _edges)
        edges = []
        for edge in _edges:
            edges.append(Edge(edge["properties"], edge["edgeNode"], edge["nodeLabel"][0]))
        print("\n", edges)
        self.edges = edges


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
        newName = self.properties.pop("name")
        self.con.rename(self.name, self.label, {'name': newName})
        self.name = newName
        self.con.merge(self.name, self.label, self.properties)
        

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