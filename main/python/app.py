import os
from dotenv import load_dotenv

from flask import Flask, flash, redirect, render_template, request, session

from helpers import Node

app = Flask(__name__)

load_dotenv()
url = "neo4j://localhost:7687"
user_ = os.environ.get("NEO4J_USER")
password_ = os.environ.get("NEO4J_PASSWORD")
con = Connection(url, user_, password_)
