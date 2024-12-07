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
        self.label = label
        self.properties = node
        edges = []
        for edge in _edges:
            edges.append({
                "properties": edge["properties"],
                "name": edge["edgeNode"],
                "label": edge["nodeLabel"]
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
            self.con.merge_edge(self.name, self.label, edge["node"], edge["label"], edge["properties"])
    
    def deleteNode(self):
        self.con.delete(self.name, self.label)
        self.name = None

    def getData(self):
        return {
            "name": self.name,
            "label": self.label,
            "properties": self.properties,
            "edges": self.properties
        }

    def saveNode(self):
        self.mergeNode()
        self.mergeEdge()