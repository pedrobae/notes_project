import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, request, jsonify, flash

from helpers import Node

from connection import Connection


app = Flask(__name__)

load_dotenv()
url = "neo4j://localhost:7687"
user_ = os.environ.get("NEO4J_USER")
password_ = os.environ.get("NEO4J_PASSWORD")
con = Connection(url, user_, password_)

activeNode = Node(con)


@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    writing = request.args.get('q')
    search = con.search_node(writing)
    results = [node["name"] for node in search]
    return jsonify(matching_results = results)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/setNode", methods=["POST"])
def setNode():
    data = None
    if request.method == "POST":
        print("Called /activate POST")
        name = request.form.get("search")
        print("\n\n\n",name)
        activeNode.setNode(name)
        data = activeNode.getData()
        print(data)
    
    return render_template("index.html", activeNode = data)

if __name__ == "__main__":
    app.run(debug=True)