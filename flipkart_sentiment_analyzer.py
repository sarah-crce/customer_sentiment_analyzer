from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch
import pandas as pd
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import os

# batch_size = 5

def flipkart_sentiment():
  data = pd.read_csv('flipkart_data.csv')
  reviews = data['Review'].tolist()
  i = 0 
  # print(reviews)

  roberta = "cardiffnlp/twitter-roberta-base-sentiment"

  model = AutoModelForSequenceClassification.from_pretrained(roberta)

  tokenizer = AutoTokenizer.from_pretrained(roberta)

  labels = ['Negative', 'Neutral', 'Positive']
  sentiments = []

  for sentence in reviews:
    encoded_tweet = tokenizer(sentence, return_tensors='pt')

    output = model(**encoded_tweet)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)


    if(scores[i]>scores[i+1] and scores[i]>scores[i+2]):
        l = labels[i]
        i=0
    elif(scores[i+1]>scores[i] and scores[i+1]>scores[i+2]):
        l = labels[i+1]
        i=0
    else:
        l = labels[i+2]
        i=0


    sentiments.append(l)

  df = pd.DataFrame(sentiments, columns = ['Sentiment'])
  print(df)

  data['Sentiments'] = df
  data.to_csv('output_flipkart.csv', index=False)

  cwd = os.getcwd()
  print(cwd)
  csv_url = cwd+'\output_flipkart.csv'
  print(csv_url)

  cloudinary.config(
    cloud_name = "do7wdh1hr",
    api_key = "466235919311831",
    api_secret = "jGLXkaC36AfmlhSHKmuDSRgoL6o",
    secure = True
  )



  # Upload CSV file to Cloudinary
  def upload_csv_to_cloudinary(csv_file_path):
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(csv_file_path, resource_type='raw')

        # Print the result containing the file URL
        print("File uploaded successfully. URL:", result['secure_url'])
        url=result['secure_url']
        return url
    except Exception as e:
        print("Error uploading file:", str(e))
        return str(e)



  # Call the function to upload the CSV file to Cloudinary
  send_url=upload_csv_to_cloudinary(csv_url)
  return send_url













