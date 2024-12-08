class Node():
    def __init__(self, con):
        self.con = con
        self.name = None
        self.label = None
        self.properties = {}
        self.edges = []

    def setNode(self, name):
        if self.name:
            self.saveNode()

        self.name = name
        node, label, _edges = self.con.read(name)
        self.label = label[0]
        self.properties = node
        edges = []
        for edge in _edges:
            edges.append({
                "properties": edge["properties"],
                "name": edge["edgeNode"],
                "label": edge["nodeLabel"][0]
            })
        self.edges = edges

    def updateNode(self, properties):
        self.properties = properties

    def updateEdges(self, edges):
        self.edges = edges

    def mergeNode(self):
        self.con.merge(self.name, self.label, self.properties)
        self.name = self.properties["name"]

    def mergeEdge(self):
        for edge in self.edges:
            self.con.merge_edge(self.name, self.label, edge["name"], edge["label"], edge["properties"])
    
    def deleteNode(self):
        self.con.delete(self.name, self.label)
        self.name = None

    def getData(self):
        # Changing the structure of properties to suit the jinja in index.html
        properties_list = []
        for property, value in self.properties.items():
            properties_list.append([property, value])

        return {
            "name": self.name,
            "label": self.label,
            "properties": properties_list,
            "edges": self.edges
        }

    def saveNode(self):
        self.mergeNode()
        self.mergeEdge()