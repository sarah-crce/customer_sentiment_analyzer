from flask import Flask, request, render_template
import re
from Query_Execution.db_query import execute_query, query_to_find
from Product_Fetch.flipkart_scrape import flipkart_data
from Product_Fetch.flipkart_sentiment_analyzer import flipkart_sentiment
from Query_Execution.db_store import graph_db
from Product_Fetch.tweet_sentiment_analyzer import tweet_sentiment
from Product_Fetch.twitter_scrape import tweet_scrape

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
        query_flag=query_to_find(search_product[0][0],search_product[0][1])
        if query_flag == True:
            executed_query=execute_review_query(english_query, search_product[0][1])
            if(isinstance(executed_query, str)):
                return render_template('index.html', image=executed_query)
            return render_template('index.html', headers=executed_query[1], table_data=executed_query[0])
        else:
            search_brand= english_query.split("brand")
            tw_search = search_product[0][1]+search_brand[1]
            tw_data=tweet_scrape(search_product[0][0],tw_search, search_product[0][1])
            fl_data = flipkart_data(search_product[0][0],search_brand[1],search_product[0][1])
            if(tw_data or fl_data == False):
                print("Some data not available")
                if(tw_data==True):
                    sentiment_analysis('tw')
                elif(fl_data==True):
                    sentiment_analysis('fl')
            else:
                sentiment_analysis()
            executed_query=execute_review_query(english_query, search_product[0][1])
            print(executed_query)
            if(isinstance(executed_query, str)):
                return render_template('index.html', image=executed_query)
            return render_template('index.html', headers=executed_query[1], table_data=executed_query[0])

        
def sentiment_analysis(social_media_source):
    if(social_media_source=='tw'):
        tw_url=tweet_sentiment()
        add_tw_to_graph = graph_db(tw_url)
    elif(social_media_source=='fl'):
        fl_url=flipkart_sentiment()
        add_fl_to_graph = graph_db(fl_url)
    else:
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
        