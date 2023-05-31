from Product_Fetch.code_reuse import create_df_sentiment, csv_file_handling, sentiment_analyzer, store_in_cloudinary


def tweet_sentiment():
  data = csv_file_handling(None, 'twitter_data.csv', 'read')
  reviews = data['Review'].tolist()

  sentiments = sentiment_analyzer(reviews)
  df = create_df_sentiment(sentiments)

  data['Sentiments'] = df

  csv_file = csv_file_handling(data, 'tw_sentiments.csv', 'write')
  print(csv_file)

  csv_cloudinary_url = store_in_cloudinary(csv_file)

  return csv_cloudinary_url

# url = tweet_sentiment()
# print(url)






