import snscrape.modules.twitter as sntwitter
import re
from Product_Fetch.code_reuse import create_df_product, csv_file_handling


def tweet_scrape(product_type,query_portion, product_name):
   query = query_portion+" HPIndia -from:HPIndia -filter:replies -filter:links -filter:media -lang:hi"
   tweets = []
   limit = 100

   for tweet in sntwitter.TwitterSearchScraper(query).get_items():
      if len(tweets) == limit:
         break
      else:
         tweets.append([product_type, product_name, tweet.content])

   def change_mentions_to_user(tweet):
      changed = re.sub(r'@(\w+)', r'@user', tweet)
      return changed


   for i in range(len(tweets)):
      tweets[i][2] = change_mentions_to_user(tweets[i][2])


   df = create_df_product(tweets)

   if len(df)==0:
      return False
   
   csv_file = csv_file_handling(df, 'twitter_data.csv' ,'write')
   return True


# tweet_scrape('monitor','HP monitor', 'general')

   


