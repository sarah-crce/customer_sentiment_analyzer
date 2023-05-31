from neo4j import GraphDatabase

def connection():
    uri = "neo4j+s://321eaff0.databases.neo4j.io"
    username = "neo4j"
    password = "Eob2hHw249f40DbLGgR1qx_TELhXg5S4g-1dnga_D7c"
    graph = GraphDatabase.driver(uri, auth=(username, password))
    return graph