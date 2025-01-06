import os
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify

from helpers import Node, Edge

from connection import Connection


app = Flask(__name__)

load_dotenv()
uri = "bolt://neo4j:7687"
user_ = os.environ.get("NEO4J_USER")
password_ = os.environ.get("NEO4J_PASSWORD")
con = Connection(uri, user_, password_)

activeNode = Node(con)


@app.route('/getData', methods=['GET'])
def getData():
    data = activeNode.getData()
    print(data)
    return jsonify(data = data)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    writing = request.args.get('q')
    search = con.search_node(writing)
    results = [node["name"] for node in search]
    print("\n autocomplete suggestions: ", results)
    return jsonify(matching_results = results)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/setNode", methods=["POST"])
def setNode():
    if request.method == "POST":
        name = request.form.get("search")
        activeNode.setNode(name)

        return getData()


@app.route("/saveNode", methods=["POST"])
def saveNode():
    try:
        form_data = request.get_json()
        print(form_data)

        edges = []
        for edge in form_data['edges']:
            edges.append(Edge(edge['properties'], 
                              edge['name'], 
                              edge["label"], 
                              edge['type']))
            
        activeNode.updateNode(form_data["label"], 
                              form_data['name'], 
                              form_data['properties'], 
                              edges)
        activeNode.saveNode()

        return jsonify({
                "success": True,
                "message": "Node data saved successfully.",
            }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error ocurred",
            "error": str(e)
        }), 500
    

@app.route("/getGraphData", methods=["GET"])
def getGraphData():
    print(activeNode.graph)
    return jsonify(activeNode.graph)


@app.route("/expandGraph", methods=["POST"])
def expandGraph():
    data = None
    if request.method == "POST":
        name = request.form.get('id')

        activeNode.setNodeExpand(name)

        data = activeNode.getData()
        
    print(data)
    return render_template("index.html", activeNode = data)


@app.route("/deleteNode", methods=["GET"])
def deleteNode():
    data = None
    if request.method == "GET":
        activeNode.deleteNode()
        activeNode.setNode("")
        data = activeNode.getData()
        print(data)

    return render_template("index.html", activeNode = data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
