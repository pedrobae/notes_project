import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, request, jsonify, flash

from helpers import Node

from connection import Connection


app = Flask(__name__)

load_dotenv()
uri = "bolt://neo4j:7687"
user_ = os.environ.get("NEO4J_USER")
password_ = os.environ.get("NEO4J_PASSWORD")
con = Connection(uri, user_, password_)

activeNode = Node(con)


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    writing = request.args.get('q')
    search = con.search_node(writing)
    results = [node["name"] for node in search]
    return jsonify(matching_results = results)


@app.route("/", methods=["GET", "POST"])
def index():
    data = activeNode.getData()
    return render_template("index.html", activeNode = data)


@app.route("/setNode", methods=["POST"])
def setNode():
    data = None
    if request.method == "POST":
        name = request.form.get("search")
        form_data = request.get_json()
        print(name,"\n\n\nReceived Form Data:", form_data)
        activeNode.setNode(name)
        data = activeNode.getData()
        print(data)
    
    return render_template("index.html", activeNode = data), jsonify({"message": "Data saved successfully!"})


@app.route("/addProperty", methods=["GET"])
def addProperty():
    data = None
    if request.method == "GET":
        activeNode.addProperty()
        data = activeNode.getData()
        print(data)

    return render_template("index.html", activeNode = data)

@app.route("/addEdge", methods=["GET"])
def addEdge():
    data = None
    if request.method == "GET":
        activeNode.addEdge()
        data = activeNode.getData()
        print(data)

    return render_template("index.html", activeNode = data)

                
@app.route("/addEdgeProperty", methods=["POST"])
def addEdgeProperty():
    data = None
    if request.method == "POST":
        i = int(request.form.get("index"))
        activeNode.edges[i].addProperty()
        data = activeNode.getData()
        print(data)

    return render_template("index.html", activeNode = data)

@app.route("/saveNode", methods=["POST"])
def saveNode():
    data = activeNode.getData()
    
    return render_template("index.html", activeNode = data)

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
