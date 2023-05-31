import pandas as pd
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

def create_df_product(review_list):
    df = pd.DataFrame(review_list, columns = ['ProductType','ProductName','Review'])
    return df

def csv_file_handling(df, csv_name, rw):
    absolute= os.path.dirname(__file__)
    relative= "CSV\\"+csv_name
    path = os.path.join(absolute, relative)
    if(rw == 'write'):
        csv_file=df.to_csv(path, index = False)
        return csv_name
    else:
        data = pd.read_csv(path)
        return data
    
def create_df_sentiment(sentiments):
    df = pd.DataFrame(sentiments, columns = ['Sentiment'])
    return df

def sentiment_analyzer(reviews):
    i = 0 
    sentiments = []
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    labels = ['Negative', 'Neutral', 'Positive']
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
    return sentiments

def store_in_cloudinary(csv_name):
    cwd = os.getcwd()
    print(cwd)
    csv_url = cwd+'\\Product_Fetch\\CSV\\'+csv_name
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

    return upload_csv_to_cloudinary(csv_url)


