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
    try:
        search = request.get_json()
        print('\nSetting Node: ', search['search'])

        activeNode.setNode(search['search'])
        data = activeNode.getData()
        print('Node Data:', data)

        return jsonify({
                "success": True,
                "message": "Node data found successfully.",
                "nodeData": data
            }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error ocurred",
            "error": str(e)
        }), 500


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


@app.route("/deleteNode", methods=["GET"])
def deleteNode():
    try:
        activeNode.deleteNode()
        activeNode.setNode("")
        data = activeNode.getData()
        print(data)

        return jsonify({
                "success": True,
                "message": "Node deleted successfully",
                'activeNode': data
            }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error ocurred",
            "error": str(e)
        }), 500
    

@app.route("/getGraphData", methods=["GET"])
def getGraphData():
    try:
        print('\nGraph Data: ', activeNode.graph)
        return jsonify({
                "success": True,
                "message": "Graph data found successfully.",
                "graphData": activeNode.graph
            }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error ocurred",
            "error": str(e)
        }), 500


@app.route("/expandGraph", methods=["POST"])
def expandGraph():
    try:
        clickedNode = request.get_json()
        print('\nClicked Node', clickedNode)
        activeNode.setNodeExpand(clickedNode['id'])
        print('\nGraph Data: ', activeNode.graph)
        return jsonify({
                "success": True,
                "message": "Graph expanded successfully.",
                "graphData": activeNode.graph
            }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "An error ocurred",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
