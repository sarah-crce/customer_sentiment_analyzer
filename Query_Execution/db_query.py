from tabulate import tabulate
import matplotlib.pyplot as plt
import cloudinary
import os 
from Query_Execution.db_connection import connection

def execute_query(find, product):

  driver = connection()

  # Parse CSV and import data into Neo4j
  with driver.session() as session:
    if(find=="problem"):
      cypher_query=f'''
      MATCH (n:ProductName {{name: '{product}'}})-[:NEGATIVE]->(r:Review)
        RETURN n.name AS Product, r.content AS Problem
      '''
      res = session.run(cypher_query)
      table_data = [(data["Product"], data["Problem"]) for data in res]
 
      headers = ["Product", "Problem"]

      print(tabulate(table_data, headers=headers, tablefmt="grid"))

    elif(find=="positive"):
      cypher_query=f'''
      MATCH (n:ProductName {{name: '{product}'}})-[:POSITIVE]->(r:Review)
        RETURN n.name AS Product, r.content AS Positive
      '''
      res = session.run(cypher_query)

      table_data = [(data["Product"], data["Positive"]) for data in res]
 
      headers = ["Product", "Positive"]

      print(tabulate(table_data, headers=headers, tablefmt="grid"))

    elif(product==None):
      flag = 1
      cypher_query=f'''
        MATCH (s:Sentiment)<-[:SENTIMENT]-(r:Review)
        WHERE s.name IN ['Negative', 'Positive', 'Neutral']
        WITH s.name AS Sentiment, count(r) AS TotalReviews
        RETURN Sentiment, TotalReviews
      '''
      res = session.run(cypher_query)

      x= []
      y= []
      for data in res:
        x.append(data['Sentiment'])
        y.append(data['TotalReviews'])
 
      plt.bar(x, y)
      print(x,y)
      plt.xlabel('Sentiments')
      plt.ylabel('Reviews')
      plt.title('Bar Graph')
      image=plt.savefig('graph.png')
      cwd = os.getcwd()
      print(cwd)
      img_url = cwd+'\graph.png'
      print(img_url)

      cloudinary.config(
        cloud_name = "do7wdh1hr",
        api_key = "466235919311831",
        api_secret = "jGLXkaC36AfmlhSHKmuDSRgoL6o",
        secure = True
      ) 

      try:
          # Upload the file to Cloudinary
          result = cloudinary.uploader.upload(img_url, resource_type='raw')

          # Print the result containing the file URL
          print("File uploaded successfully. URL:", result['secure_url'])
          url=result['secure_url']
          return url
      except Exception as e:
          print("Error uploading file:", str(e))

        
    else:
      cypher_query=f'''
      MATCH (n:ProductName {{name: '{product}'}})-[:NEUTRAL]->(r:Review)
        RETURN n.name AS Product, r.content AS Neutral
      '''
      res =session.run(cypher_query)

      table_data = [(data["Product"], data["Neutral"]) for data in res]
 
      headers = ["Product", "Neutral"]

      print(tabulate(table_data, headers=headers, tablefmt="grid"))

  # Close the Neo4j driver

  driver.close()

  print([table_data, headers])
  return([table_data, headers])


def query_to_find(ptype,pname):
  driver = connection()
  with driver.session() as session:

      cypher_query = f"""
        MATCH (t:ProductType {{name: '{ptype}'}})-[:NAME]->(n:ProductName {{name: '{pname}'}})
        RETURN EXISTS((t)-[:NAME]->(n)) AS hasRelation
        """
      result = session.run(cypher_query)
      for record in result:
          already_exists = record["hasRelation"]
          if already_exists:
              return True
          else:
              return False
  driver.close()
          
# ans=query_to_find('printer','deskjet')
# print(ans)






