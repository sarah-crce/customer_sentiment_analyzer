import snscrape.modules.twitter as sntwitter
import re

import urllib.parse
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import pandas as pd
import os

def tweet_scrape(query_portion, product_name):
   query = query_portion+" HPIndia -from:HPIndia -filter:replies -filter:links -filter:media -lang:hi"
   tweets = []
   limit = 10

   for tweet in sntwitter.TwitterSearchScraper(query).get_items():
      if len(tweets) == limit:
         break
      else:
         tweets.append([product_name, tweet.username, tweet.content])

   def change_mentions_to_user(tweet):
      changed = re.sub(r'@(\w+)', r'@user', tweet)
      return changed


   for i in range(len(tweets)):
      tweets[i][2] = change_mentions_to_user(tweets[i][2])


   df = pd.DataFrame(tweets, columns = ['Product', 'User', 'Review'])
   print(df)

   if df.empty:
      return False

   df.to_csv('twitter_data.csv')
   return True

   


