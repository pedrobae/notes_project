from connection import Connection

class Node():
    def __init__(self, con):
        self.con = con
        self.name = None
        self.label = None
        self.properties = {}
        self.edges = []

    def setNode(self, name, label):
        if self.name:
            self.saveNode()

        self.name = name
        self.label = label
        node, edges = self.con.read(name, label)
        self.properties = node
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

    def saveNode(self):
        self.mergeNode()
        self.mergeEdge()