from flask import Flask, redirect, request,url_for, render_template
from textblob import TextBlob
from textblob import Word
import re
from cypher_query import execute_query
from flipkart_data import flipkart_data
from flipkart_sentiment_analyzer import flipkart_sentiment
from graph_data import graph_db
from tweet_sentiment_analyzer import tweet_sentiment
import twitter_data

app = Flask(__name__)

@app.route('/')
def take_input():
    return render_template('index.html')


@app.route('/scrape',methods=['POST','GET'])
def scrape():
    
    if request.method=='POST':
        english_query=(request.form['query'])
        print(english_query)
        search_product = re.findall(r"(printer|laptop|desktop)\s+(.*?)\s+by", english_query, re.IGNORECASE)
        print(search_product[0][1])
        search_brand= english_query.split("brand")
        print(search_brand[1])
        tw_search = search_product[0][1]+search_brand[1]
        tw_data=twitter_data.tweet_scrape(tw_search, search_product[0][1])
        if(tw_data==False):
            tw_search = search_product[0][0]+search_brand[1]
            tw_data=twitter_data.tweet_scrape(tw_search, search_product[0][0])
        fl_data = flipkart_data(search_brand[1],search_product[0][1])
        if(fl_data==False):
            fl_data = flipkart_data(search_brand[1],search_product[0][0])
        
        sentiment_analysis()
        query_search= search_product[0][1] if tw_data else search_product[0][0]
        print(query_search)
        executed_query=execute_review_query(english_query, query_search)
        print(executed_query)
        if(isinstance(executed_query, str)):
            return render_template('index.html', image=executed_query)
        return render_template('index.html', headers=executed_query[1], table_data=executed_query[0])

        
def sentiment_analysis():
    tw_url=tweet_sentiment()
    fl_url=flipkart_sentiment()
    add_tw_to_graph = graph_db(tw_url)
    add_fl_to_graph = graph_db(fl_url)


def execute_review_query(english_query,query_search):
    english_lower = english_query.lower()
    find = ""
    if('problem' in english_lower):
        find='problem'
    elif('positive' in english_lower):
        find='positive'
    elif('neutral' in english_lower):
        find='neutral'
  

    if(len(find)==0):
        sentiment_result=execute_sentiment_query(english_lower)
        if(sentiment_result==False):
            print("Wrong Query")
            exit
        else:
            return sentiment_result
    else:
        executed_query=execute_query(find,query_search)
        return(executed_query)
        
    

def execute_sentiment_query(english_lower):
    if(('bargraph' in english_lower or 'bar graph' in english_lower) and 
       ('sentiment' in english_lower or 'sentiments' in english_lower)):
        find = "bargraph"
        result_url=execute_query(find,None)
        return result_url
    else:
        return False
        





    

        
        
    

        
                


      





















