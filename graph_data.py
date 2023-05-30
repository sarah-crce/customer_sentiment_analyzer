from neo4j import GraphDatabase
import chardet
import os
import csv
import requests

def graph_db(csv_url):

  uri = "neo4j+s://321eaff0.databases.neo4j.io"
  username = "neo4j"
  password = "Eob2hHw249f40DbLGgR1qx_TELhXg5S4g-1dnga_D7c"

  # Cloudinary CSV URL
  

  # Connect to Neo4j Aura
  driver = GraphDatabase.driver(uri, auth=(username, password))

  # Download CSV data from Cloudinary
  response = requests.get(csv_url)
  csv_content = response.text

  # Parse CSV and import data into Neo4j
  with driver.session() as session:

      cypher_query = f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (p:Product {{name: row.Product}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})

        MERGE (r)-[:SENTIMENT]->(s)

        WITH p, r, s
        WHERE s.name = "Negative"
        MERGE (p)-[:NEGATIVE]->(r)
        """
      cypher_query_positive= f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (p:Product {{name: row.Product}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})


        WITH p, r, s
        WHERE s.name = "Positive"
        MERGE (p)-[:POSITIVE]->(r)
        """

      cypher_query_neutral=f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (p:Product {{name: row.Product}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})


        WITH p, r, s
        WHERE s.name = "Neutral"
        MERGE (p)-[:NEUTRAL]->(r)
        """
      session.run(cypher_query, csvContent=csv_content)
      session.run(cypher_query_positive, csvContent=csv_content)
      session.run(cypher_query_neutral, csvContent=csv_content)

  # Close the Neo4j driver
  driver.close()

