import requests
from Query_Execution.db_connection import connection

def graph_db(csv_url):
  driver = connection()

  # Download CSV data from Cloudinary
  response = requests.get(csv_url)
  csv_content = response.text

  # Parse CSV and import data into Neo4j
  with driver.session() as session:

      cypher_query = f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (t:ProductType {{name: row.ProductType}})
        MERGE (n:ProductName {{name: row.ProductName}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})

        MERGE (r)-[:SENTIMENT]->(s)
        MERGE (t)-[:NAME]->(n)

        WITH n, r, s
        WHERE s.name = "Negative"
        MERGE (n)-[:NEGATIVE]->(r)
        """
      cypher_query_positive= f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (n:ProductName {{name: row.ProductName}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})


        WITH n, r, s
        WHERE s.name = "Positive"
        MERGE (n)-[:POSITIVE]->(r)
        """

      cypher_query_neutral=f"""
        LOAD CSV WITH HEADERS FROM '{csv_url}' AS row
        MERGE (n:ProductName {{name: row.ProductName}})
        MERGE (r:Review {{content: row.Review}})
        MERGE (s:Sentiment {{name: row.Sentiments}})


        WITH n, r, s
        WHERE s.name = "Neutral"
        MERGE (n)-[:NEUTRAL]->(r)
        """
      session.run(cypher_query, csvContent=csv_content)
      session.run(cypher_query_positive, csvContent=csv_content)
      session.run(cypher_query_neutral, csvContent=csv_content)

  # Close the Neo4j driver
  driver.close()

# graph_db('https://res.cloudinary.com/do7wdh1hr/raw/upload/v1685521484/op4theh0hb0bwo05e06z.csv')

