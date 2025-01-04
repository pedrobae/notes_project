import os
from dotenv import load_dotenv
from connection import Connection

if __name__ == "__main__":
    load_dotenv()
    uri = "bolt://neo4j:7687"
    user_ = os.environ.get("NEO4J_USER")
    password_ = os.environ.get("NEO4J_PASSWORD")
    con = Connection(uri, user_, password_)

#   Testing node merger
#    con.merge("Neza", "Character", {"birthYear": "10.000 B.C", "birthPlace": "Ardent Copper Empire"})
#    con.merge("Gelboss", "Character", {"shard": "Autonomy", "summary": "One of the ten genesis shards"})

#   Testing deletion
#    con.delete("Neza", "Character")

#   Testing read
    node, label, edges = con.read("")
    print(node)
    print(label)
    print(edges)

#   Testing search
#    data = con.search_node("Ne")
#    print(data)

#   Testing edge merger
#    con.merge_edge("Gelboss", "Character", "Neza", "Character", {"type": "Passion"})
#    con.merge_edge("Neza", "Character", "Death", "Character", {"type":"Herald", "summary" : "Neza proposed a bargain to become the Herald of Death in exchange for seeing her lost daughter"})

#   Closing test connection
    con.close()